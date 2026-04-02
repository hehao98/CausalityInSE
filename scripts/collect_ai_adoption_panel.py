#!/usr/bin/env python3
"""Collect longitudinal monthly panel data by cloning repos and mining git history.

Reads the repo list from data/ai_adoption_repos.csv (output of the cross-
sectional collection) and writes a single analysis-ready panel CSV covering
2024-01 through 2026-03 (27 months).  Each repo contributes 27 rows (one per
month) with:

  - commits, active_contributors  (from git log)
  - treatment_date, treatment_month, first_ai_file  (first L2+ config commit)
  - treated, months_since_treatment  (derived)
  - time-invariant covariates from the cross-sectional dataset

Supports pause/resume: repos already present in the output CSV are skipped.

Usage:
  python scripts/collect_ai_adoption_panel.py
  python scripts/collect_ai_adoption_panel.py --workers 4 --clone-dir /scratch/repos

Output:
  data/ai_adoption_panel.csv
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

from log_utils import setup_logging

log = setup_logging()

# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
REPOS_CSV = os.path.join(DATA_DIR, "ai_adoption_repos.csv")
PANEL_CSV = os.path.join(DATA_DIR, "ai_adoption_panel.csv")

DEFAULT_CLONE_DIR = os.path.join(PROJECT_ROOT, "data/repos")

# ── Panel window ─────────────────────────────────────────────────────────────

PANEL_START = "2024-01"
PANEL_END = "2026-03"


def _month_range(start: str, end: str) -> list[str]:
    """Generate YYYY-MM strings from start to end (inclusive)."""
    months = []
    y, m = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    while (y, m) <= (ey, em):
        months.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return months


ALL_MONTHS = set(_month_range(PANEL_START, PANEL_END))
SORTED_MONTHS = sorted(ALL_MONTHS)

# ── Panel columns (fixed order for CSV output) ──────────────────────────────

PANEL_FIELDS = [
    "full_name", "month",
    # outcome + git-based confounder
    "commits", "active_contributors",
    # GHArchive confounders (filled later via BigQuery; empty during collection)
    "new_stars", "new_issues", "new_forks", "prs_merged", "new_releases",
    # treatment
    "treatment_date", "treatment_month", "first_ai_file",
    "treated", "months_since_treatment",
    # time-invariant covariates (from cross-sectional data)
    "owner_type", "queried_language", "primary_language",
    "created_at", "license", "ai_maturity_level",
]

# ── AI maturity classification (mirrors collect_ai_adoption_data.py) ─────────

L4_RE = [re.compile(p) for p in [
    r"^\.claude/agents/", r"^\.claude/handoffs/",
    r"^\.docker/mounts/\.claude/",
    r"^\.github/actions/write-claude-execution-report/",
    r"^mcp-docker\.json$", r"^mcp-local\.json$",
]]

L3_RE = [re.compile(p) for p in [
    r"^\.claude/commands/", r"^\.claude/skills/", r"^\.claude/workflows/",
    r"^\.claude/plan-.*\.md$", r"^\.github/.+/prompts/",
    r"^\.github/ai-triaging/", r"^\.github/claude-docs-auditor/",
]]

L2_RE = [re.compile(p) for p in [
    r"^CLAUDE\.md$", r"^\.claude/settings\.json$",
    r"^\.claude/settings\.local\.json$", r"^\.claude/architecture\.md$",
    r"^\.claude/rules/", r"^\.claude/knowledge/", r"^\.claude/archive/",
    r"^\.claude/output-styles/",
    r"^\.cursorrules$", r"^(.+/)?\.cursor/rules/",
    r"^(.+/)?\.cursor/mcp\.json$",
    r"^\.github/copilot-instructions\.md$", r"^AGENTS\.md$", r"^\.mcp\.json$",
]]


def classify_path(path: str) -> int | None:
    """Return 4, 3, or 2 if *path* matches an AI config pattern, else None."""
    for pat in L4_RE:
        if pat.match(path):
            return 4
    for pat in L3_RE:
        if pat.match(path):
            return 3
    for pat in L2_RE:
        if pat.match(path):
            return 2
    return None


# Broad git pathspecs for the treatment-timing search.  classify_path() does
# the precise matching on the files that git returns.
AI_PATHSPECS = [
    "CLAUDE.md", "AGENTS.md", ".cursorrules", ".mcp.json",
    ".claude", ".cursor",
    ".github/copilot-instructions.md",
    ".windsurfrules",
    ".docker/mounts/.claude",
    ".github/actions/write-claude-execution-report",
    ".github/prompts", ".github/ai-triaging", ".github/claude-docs-auditor",
    "mcp-docker.json", "mcp-local.json",
]

# ── Git helpers ──────────────────────────────────────────────────────────────


def _run_git(clone_dir: str, *args: str, timeout: int = 120) -> str:
    """Run a git command in *clone_dir* and return stdout."""
    cmd = ["git", "-C", clone_dir] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, result.stdout, result.stderr,
        )
    return result.stdout


MAX_CLONE_RETRIES = 3


def clone_repo(full_name: str, clone_dir: str) -> bool:
    """Bare blobless clone from GitHub with retries.  Returns True on success."""
    url = f"https://github.com/{full_name}.git"
    for attempt in range(1, MAX_CLONE_RETRIES + 1):
        # Clean up any partial clone from a previous failed attempt
        if os.path.isdir(clone_dir):
            shutil.rmtree(clone_dir)
        try:
            subprocess.run(
                ["git", "clone", "--filter=blob:none", "--bare", url, clone_dir],
                capture_output=True, text=True, timeout=600, check=True,
            )
            return True
        except subprocess.TimeoutExpired:
            log.warning("Clone timed out for %s (attempt %d/%d)",
                        full_name, attempt, MAX_CLONE_RETRIES)
        except subprocess.CalledProcessError as e:
            msg = e.stderr[:200] if e.stderr else str(e)
            log.warning("Clone failed for %s (attempt %d/%d): %s",
                        full_name, attempt, MAX_CLONE_RETRIES, msg)
        if attempt < MAX_CLONE_RETRIES:
            time.sleep(2 ** attempt)
    # All retries exhausted — clean up any partial directory
    if os.path.isdir(clone_dir):
        shutil.rmtree(clone_dir)
    return False


# ── Extraction ───────────────────────────────────────────────────────────────


def extract_monthly_data(clone_dir: str) -> dict[str, dict]:
    """Monthly commits and unique contributors from ``git log``.

    Uses committer-date ``--after/--before`` with a 1-month buffer, then
    buckets precisely by author date (``%aI``).

    Returns ``{month: {"commits": int, "active_contributors": int}}``.
    """
    try:
        raw = _run_git(
            clone_dir, "log", "HEAD",
            "--format=%aI|%ae",
            # 1-month buffer around panel window to handle committer/author
            # date mismatches at boundaries.
            "--after=2023-11-30", "--before=2026-05-01",
            timeout=300,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return {}

    monthly_commits: dict[str, int] = defaultdict(int)
    monthly_authors: dict[str, set[str]] = defaultdict(set)

    for line in raw.split("\n"):
        line = line.strip()
        if not line or "|" not in line:
            continue
        date_str, email = line.split("|", 1)
        month = date_str[:7]  # YYYY-MM from ISO-8601 author date
        if month in ALL_MONTHS:
            monthly_commits[month] += 1
            monthly_authors[month].add(email.strip().lower())

    result = {}
    for m in SORTED_MONTHS:
        result[m] = {
            "commits": monthly_commits.get(m, 0),
            "active_contributors": len(monthly_authors.get(m, set())),
        }
    return result


def extract_treatment_timing(clone_dir: str) -> dict:
    """Find the earliest commit that **added** an L2+ AI config file.

    Returns ``{"treatment_date": ..., "treatment_month": ...,
    "first_ai_file": ...}`` (empty strings if nothing found).
    """
    empty = {"treatment_date": "", "treatment_month": "", "first_ai_file": ""}
    try:
        raw = _run_git(
            clone_dir, "log", "HEAD",
            "--diff-filter=A", "--name-only", "--reverse",
            "--format=COMMIT|%H|%aI",
            "--", *AI_PATHSPECS,
            timeout=300,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return empty

    if not raw.strip():
        return empty

    # Output format (oldest first thanks to --reverse):
    #   COMMIT|<hash>|<author-date>
    #                                    ← blank line
    #   <filename>
    #   ...
    current_date = ""
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("COMMIT|"):
            _, _, current_date = line.split("|", 2)
        else:
            level = classify_path(line)
            if level is not None and level >= 2:
                return {
                    "treatment_date": current_date,
                    "treatment_month": current_date[:7],
                    "first_ai_file": line,
                }

    return empty


# ── Per-repo pipeline ────────────────────────────────────────────────────────


def _months_since(treatment_month: str, month: str) -> int:
    """Signed integer distance in months (negative = pre-treatment)."""
    ty, tm = map(int, treatment_month.split("-"))
    my, mm = map(int, month.split("-"))
    return (my - ty) * 12 + (mm - tm)


def process_repo(
    full_name: str,
    clone_base: str,
    repo_covariates: dict,
) -> tuple[str, list[dict]]:
    """Clone (if needed) and build complete panel rows for one repo.

    Returns ``(full_name, rows)`` where *rows* is a list of 27 dicts (one
    per panel month), each containing every column in ``PANEL_FIELDS``.
    On clone failure, returns an empty list.
    """
    safe_name = full_name.replace("/", "__")
    clone_dir = os.path.join(clone_base, safe_name + ".git")

    # Clone if not already present (allows resume without re-downloading)
    if not os.path.isdir(clone_dir):
        if not clone_repo(full_name, clone_dir):
            return full_name, []

    # Monthly commits + contributors
    monthly = extract_monthly_data(clone_dir)

    # Treatment timing
    treatment = extract_treatment_timing(clone_dir)
    t_date = treatment["treatment_date"]
    t_month = treatment["treatment_month"]
    t_file = treatment["first_ai_file"]

    rows = []
    for m in SORTED_MONTHS:
        data = monthly.get(m, {"commits": 0, "active_contributors": 0})
        treated = 1 if (t_month and m >= t_month) else 0
        mst = _months_since(t_month, m) if t_month else ""
        row = {
            "full_name": full_name,
            "month": m,
            "commits": data["commits"],
            "active_contributors": data["active_contributors"],
            # GHArchive columns — placeholders; filled by BigQuery join later
            "new_stars": "",
            "new_issues": "",
            "new_forks": "",
            "prs_merged": "",
            "new_releases": "",
            "treatment_date": t_date,
            "treatment_month": t_month,
            "first_ai_file": t_file,
            "treated": treated,
            "months_since_treatment": mst,
        }
        row.update(repo_covariates)
        rows.append(row)

    return full_name, rows


# ── Resume support ───────────────────────────────────────────────────────────


def load_processed_repos(csv_path: str) -> set[str]:
    """Return full_name values already present in a CSV."""
    if not os.path.exists(csv_path):
        return set()
    try:
        df = pd.read_csv(csv_path, usecols=["full_name"])
        return set(df["full_name"].unique())
    except Exception:
        return set()


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--workers", type=int, default=8,
        help="Parallel clone/extract workers (default: 8)",
    )
    parser.add_argument(
        "--clone-dir", type=str, default=DEFAULT_CLONE_DIR,
        help=f"Directory for bare clones (default: {DEFAULT_CLONE_DIR})",
    )
    args = parser.parse_args()

    # ── Load repo list ───────────────────────────────────────────────────────
    if not os.path.exists(REPOS_CSV):
        log.error("Repo list not found: %s", REPOS_CSV)
        sys.exit(1)

    repos_df = pd.read_csv(REPOS_CSV)
    all_repos = repos_df["full_name"].tolist()
    log.info("Loaded %d repos from %s", len(all_repos), REPOS_CSV)

    # Build a lookup of time-invariant covariates per repo
    covariate_cols = [
        "owner_type", "queried_language", "primary_language",
        "created_at", "license", "ai_maturity_level",
    ]
    covariate_cols = [c for c in covariate_cols if c in repos_df.columns]
    repo_cov_lookup: dict[str, dict] = {}
    for _, row in repos_df.iterrows():
        repo_cov_lookup[row["full_name"]] = {c: row[c] for c in covariate_cols}

    # ── Resume ───────────────────────────────────────────────────────────────
    processed = load_processed_repos(PANEL_CSV)
    if processed:
        log.info("Resuming: %d repos already in panel", len(processed))

    remaining = [r for r in all_repos if r not in processed]
    log.info("Repos to process: %d", len(remaining))

    if not remaining:
        log.info("All repos already processed — nothing to do")
        return

    # ── Prepare output ───────────────────────────────────────────────────────
    os.makedirs(args.clone_dir, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    if not processed:
        pd.DataFrame(columns=PANEL_FIELDS).to_csv(PANEL_CSV, index=False)

    # ── Process repos ────────────────────────────────────────────────────────
    completed = len(processed)
    failed = 0
    row_buf: list[dict] = []

    def flush():
        nonlocal row_buf
        if row_buf:
            pd.DataFrame(row_buf, columns=PANEL_FIELDS).to_csv(
                PANEL_CSV, mode="a", header=False, index=False)
            row_buf = []

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    process_repo, repo, args.clone_dir,
                    repo_cov_lookup.get(repo, {}),
                ): repo
                for repo in remaining
            }
            for future in as_completed(futures):
                repo = futures[future]
                try:
                    full_name, rows = future.result()
                except Exception:
                    log.exception("Unhandled error for %s", repo)
                    failed += 1
                    continue

                if not rows:
                    log.warning("No data for %s (clone may have failed)",
                                full_name)
                    failed += 1
                    continue

                row_buf.extend(rows)
                completed += 1

                total_commits = sum(r["commits"] for r in rows)
                t_month = rows[0].get("treatment_month") or "never"
                log.info(
                    "[%d/%d] %s  commits=%d  treated=%s",
                    completed, len(all_repos), full_name, total_commits,
                    t_month,
                )

                # Flush every 10 repos
                if completed % 10 == 0:
                    flush()

    except KeyboardInterrupt:
        log.info("Interrupted — flushing partial progress")
    finally:
        flush()

    log.info("Done. %d processed (%d failed). Output: %s",
             completed, failed, PANEL_CSV)


if __name__ == "__main__":
    main()
