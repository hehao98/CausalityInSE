#!/usr/bin/env python3
"""Run SonarQube analysis on the latest commit of each repo in the AI adoption dataset.

For each repo in data/ai_adoption_repos.csv, this script:
1. Shallow-clones the repo (--depth 1) to save disk space
2. Runs sonar-scanner on the working tree
3. Fetches the resulting metrics from the SonarQube API
4. Writes one row per repo to data/ai_adoption_sonarqube.csv

Repos are processed in parallel (default 8 workers).
Already-analysed repos are skipped on re-run.

Usage:
  python scripts/run_sonarqube.py                  # all repos
  python scripts/run_sonarqube.py --limit 10       # first 10 repos only
  python scripts/run_sonarqube.py --cleanup        # delete clones after each repo

Environment (reads from .env):
  SONAR_SCANNER_PATH  — path to sonar-scanner binary
  SONAR_TOKEN         — SonarQube auth token
  SONAR_HOST          — SonarQube server URL (e.g. http://localhost:9000)
  GITHUB_TOKEN        — (optional) for cloning private repos

Output:
  data/ai_adoption_sonarqube.csv
"""

import argparse
import csv
import os
import shutil
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import requests
from dotenv import load_dotenv

from log_utils import setup_logging

log = setup_logging()

# ── Paths & Config ───────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

SONAR_SCANNER = os.environ.get("SONAR_SCANNER_PATH", "sonar-scanner")
SONAR_TOKEN = os.environ.get("SONAR_TOKEN", "")
SONAR_HOST = os.environ.get("SONAR_HOST", "http://localhost:9000")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

DATA_DIR = PROJECT_ROOT / "data"
REPOS_CSV = DATA_DIR / "ai_adoption_repos.csv"
OUTPUT_CSV = DATA_DIR / "ai_adoption_sonarqube.csv"
CLONE_DIR = PROJECT_ROOT / "data" / "repos"

# SonarQube metrics to collect
METRICS = [
    "ncloc",
    "bugs",
    "vulnerabilities",
    "code_smells",
    "duplicated_lines_density",
    "comment_lines_density",
    "cognitive_complexity",
    "software_quality_maintainability_remediation_effort",
]

# Repos known to be problematic for SonarQube (hang, crash, etc.)
REPO_IGNORE = set()

# Top 5% largest repos by size_kb are skipped automatically (computed at
# runtime from the input CSV).  This avoids cloning multi-GB repos that
# would fill the disk and take hours to scan.
SIZE_PERCENTILE_CUTOFF = 0.95

OUTPUT_FIELDS = [
    "full_name", "primary_language", "ai_maturity_level",
    "scan_success",
] + METRICS


# ── SonarQube helpers ────────────────────────────────────────────────────────

def sonar_api(endpoint: str, params: dict | None = None) -> dict:
    """GET from SonarQube API."""
    url = f"{SONAR_HOST}{endpoint}"
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    resp = requests.get(url, headers=headers, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def project_exists(project_key: str) -> bool:
    """Check whether a SonarQube project already has at least one analysis."""
    try:
        data = sonar_api("/api/project_analyses/search",
                         {"project": project_key, "ps": 1})
        return len(data.get("analyses", [])) > 0
    except requests.exceptions.RequestException:
        return False


def get_metrics(project_key: str) -> dict | None:
    """Fetch the latest metrics for a project from SonarQube."""
    try:
        data = sonar_api("/api/measures/component", {
            "component": project_key,
            "metricKeys": ",".join(METRICS),
        })
        measures = data.get("component", {}).get("measures", [])
        return {m["metric"]: m["value"] for m in measures}
    except requests.exceptions.RequestException as e:
        log.error("Failed to fetch metrics for %s: %s", project_key, e)
        return None


def delete_project(project_key: str):
    """Delete a SonarQube project to free server-side resources."""
    try:
        url = f"{SONAR_HOST}/api/projects/delete"
        headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
        requests.post(url, headers=headers, data={"project": project_key}, timeout=30)
    except requests.exceptions.RequestException:
        pass  # best-effort cleanup


# ── Git helpers ──────────────────────────────────────────────────────────────

def shallow_clone(full_name: str, dest: Path) -> bool:
    """Shallow-clone a GitHub repo (depth=1) to dest.  Returns True on success."""
    if dest.exists():
        log.info("  Clone already exists: %s", dest)
        return True

    if GITHUB_TOKEN:
        url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/{full_name}.git"
    else:
        url = f"https://github.com/{full_name}.git"

    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "--single-branch", url, str(dest)],
            capture_output=True, text=True, check=True, timeout=600,
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        stderr = getattr(e, "stderr", "") or ""
        log.error("  Clone failed for %s: %s", full_name, stderr[:200])
        # Clean up partial clone
        if dest.exists():
            shutil.rmtree(dest, ignore_errors=True)
        return False


# ── SonarQube scan ───────────────────────────────────────────────────────────

def run_scan(repo_path: Path, project_key: str) -> bool:
    """Run sonar-scanner on a repo directory.  Returns True on success."""
    cmd = [
        SONAR_SCANNER,
        f"-Dsonar.projectKey={project_key}",
        f"-Dsonar.projectName={project_key}",
        "-Dsonar.projectVersion=latest",
        "-Dsonar.sources=.",
        "-Dsonar.java.binaries=.",
        f"-Dsonar.host.url={SONAR_HOST}",
        f"-Dsonar.token={SONAR_TOKEN}",
        "-Dsonar.scm.disabled=true",
        "-Dsonar.sourceEncoding=UTF-8",
    ]
    try:
        subprocess.run(
            cmd, cwd=repo_path, capture_output=True, text=True,
            check=True, timeout=1800,  # 30-minute timeout per scan
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        stderr = getattr(e, "stderr", "") or ""
        log.error("  Scan failed for %s: %s", project_key, stderr[-300:])
        return False


# ── Main pipeline ────────────────────────────────────────────────────────────

def load_completed(csv_path: Path) -> tuple[set[str], set[str]]:
    """Load results from the output CSV for resume support.

    Returns (completed, needs_retry):
      - completed: repos with scan_success == "true" or "skipped_too_large"
        (do not re-process)
      - needs_retry: repos with scan_success == "metrics_unavailable"
        (scan was done but metrics weren't ready; retry fetching metrics)
    """
    if not csv_path.exists():
        return set(), set()
    completed = set()
    needs_retry = set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            name = r.get("full_name", "")
            status = r.get("scan_success", "")
            if status == "metrics_unavailable":
                needs_retry.add(name)
            elif name:
                completed.add(name)
    return completed, needs_retry


def rewrite_csv_without(csv_path: Path, names_to_remove: set[str]):
    """Remove rows for repos that need retrying so they can be re-appended."""
    if not csv_path.exists() or not names_to_remove:
        return
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            if r.get("full_name") not in names_to_remove:
                rows.append(r)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    log.info("Removed %d metrics_unavailable rows from %s for retry",
             len(names_to_remove), csv_path)


def process_repo(task: dict) -> dict | None:
    """Process a single repo: clone, scan, fetch metrics.

    Designed to run in a worker process.  Returns a result row dict,
    or None if the repo was already completed / should be skipped entirely
    (caller handles the skip-counting).
    """
    repo = task["repo"]
    idx = task["idx"]
    total = task["total"]
    is_retry = task["is_retry"]
    skip_scan = task["skip_scan"]
    cleanup = task["cleanup"]
    max_size_kb = task["max_size_kb"]

    full_name = repo["full_name"]
    project_key = full_name.replace("/", "_")

    # Skip ignored repos
    if full_name in REPO_IGNORE:
        log.info("[%d/%d] Skipping %s (in ignore list)", idx, total, full_name)
        return None

    # Skip repos that exceed size cutoff
    size_kb = int(repo.get("size_kb", 0) or 0)
    if size_kb > max_size_kb:
        log.info("[%d/%d] Skipping %s (%.1f MB > %.1f MB cutoff)",
                 idx, total, full_name, size_kb / 1e3, max_size_kb / 1e3)
        return {
            "full_name": full_name,
            "primary_language": repo.get("primary_language", ""),
            "ai_maturity_level": repo.get("ai_maturity_level", ""),
            "scan_success": "skipped_too_large",
        }

    log.info("[%d/%d] %s%s (%s, %.1f MB)",
             idx, total,
             "Retrying metrics for " if is_retry else "Processing ",
             full_name,
             repo.get("primary_language", "?"), size_kb / 1e3)

    row = {
        "full_name": full_name,
        "primary_language": repo.get("primary_language", ""),
        "ai_maturity_level": repo.get("ai_maturity_level", ""),
        "scan_success": "false",
    }

    clone_path = CLONE_DIR / project_key

    if is_retry:
        metrics = get_metrics(project_key)
        if metrics:
            row.update(metrics)
            row["scan_success"] = "true"
            log.info("  Retry succeeded for %s", full_name)
        else:
            row["scan_success"] = "metrics_unavailable"
            log.warning("  Metrics still unavailable for %s", full_name)
    elif skip_scan:
        if project_exists(project_key):
            metrics = get_metrics(project_key)
            if metrics:
                row.update(metrics)
                row["scan_success"] = "true"
                log.info("  Fetched existing metrics for %s", full_name)
        else:
            log.info("  No existing analysis for %s", full_name)
    else:
        if project_exists(project_key):
            log.info("  Analysis already exists in SonarQube, fetching metrics")
            metrics = get_metrics(project_key)
            if metrics:
                row.update(metrics)
                row["scan_success"] = "true"
        else:
            if not shallow_clone(full_name, clone_path):
                row["scan_success"] = "clone_failed"
                return row

            scan_ok = run_scan(clone_path, project_key)
            if scan_ok:
                time.sleep(5)
                metrics = get_metrics(project_key)
                if metrics:
                    row.update(metrics)
                    row["scan_success"] = "true"
                else:
                    row["scan_success"] = "metrics_unavailable"
                    log.warning("  Scan succeeded but metrics not yet available for %s",
                                full_name)
            else:
                row["scan_success"] = "scan_failed"

            if cleanup and clone_path.exists():
                shutil.rmtree(clone_path, ignore_errors=True)
                log.info("  Cleaned up clone for %s", full_name)

    log.info("  Done %s [%s]", full_name, row["scan_success"])
    return row


NUM_WORKERS = 8


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=0,
                        help="Process only the first N repos (0 = all)")
    parser.add_argument("--cleanup", action="store_true",
                        help="Delete each clone after scanning to save disk")
    parser.add_argument("--skip-scan", action="store_true",
                        help="Skip scanning, only fetch metrics for existing projects")
    parser.add_argument("--workers", type=int, default=NUM_WORKERS,
                        help=f"Number of parallel workers (default {NUM_WORKERS})")
    args = parser.parse_args()

    # Validate environment
    if not SONAR_TOKEN:
        log.error("SONAR_TOKEN not set in .env — aborting")
        sys.exit(1)

    CLONE_DIR.mkdir(parents=True, exist_ok=True)

    # Load input repos
    repos = []
    with open(REPOS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            repos.append(r)
    log.info("Loaded %d repos from %s", len(repos), REPOS_CSV)

    if args.limit > 0:
        repos = repos[:args.limit]
        log.info("Limiting to first %d repos", args.limit)

    # Compute size cutoff: skip the top 5% largest repos
    sizes = sorted(int(r.get("size_kb", 0) or 0) for r in repos)
    cutoff_idx = int(len(sizes) * SIZE_PERCENTILE_CUTOFF)
    max_size_kb = sizes[min(cutoff_idx, len(sizes) - 1)]
    log.info("Size cutoff (p%.0f): %.1f MB — repos larger than this will be skipped",
             SIZE_PERCENTILE_CUTOFF * 100, max_size_kb / 1e3)

    # Resume support: skip completed, retry metrics_unavailable
    completed, needs_retry = load_completed(OUTPUT_CSV)
    if completed:
        log.info("Resuming: %d repos completed, %d need metrics retry",
                 len(completed), len(needs_retry))
    if needs_retry:
        rewrite_csv_without(OUTPUT_CSV, needs_retry)

    # Build task list — filter out already-completed repos
    tasks = []
    for i, repo in enumerate(repos):
        full_name = repo["full_name"]
        if full_name in completed:
            continue
        tasks.append({
            "repo": repo,
            "idx": i + 1,
            "total": len(repos),
            "is_retry": full_name in needs_retry,
            "skip_scan": args.skip_scan,
            "cleanup": args.cleanup,
            "max_size_kb": max_size_kb,
        })

    log.info("Processing %d repos with %d workers", len(tasks), args.workers)

    # Open output CSV in append mode
    file_exists = OUTPUT_CSV.exists() and len(completed) > 0
    out_f = open(OUTPUT_CSV, "a", newline="", encoding="utf-8")
    writer = csv.DictWriter(out_f, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
    if not file_exists:
        writer.writeheader()

    total_done = len(completed)
    total_skipped = 0
    total_failed = 0

    try:
        with Pool(processes=args.workers) as pool:
            for row in pool.imap_unordered(process_repo, tasks):
                if row is None:
                    total_skipped += 1
                    continue

                writer.writerow(row)
                out_f.flush()

                status = row["scan_success"]
                if status in ("scan_failed", "clone_failed"):
                    total_failed += 1
                elif status == "skipped_too_large":
                    total_skipped += 1
                else:
                    total_done += 1

                log.info("  Progress: %d done, %d skipped, %d failed",
                         total_done, total_skipped, total_failed)

    except KeyboardInterrupt:
        log.info("Interrupted — progress saved (%d done)", total_done)
    finally:
        out_f.close()

    log.info("Finished. %d done, %d skipped, %d failed. Output: %s",
             total_done, total_skipped, total_failed, OUTPUT_CSV)


if __name__ == "__main__":
    main()
