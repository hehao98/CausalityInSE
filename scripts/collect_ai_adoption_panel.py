#!/usr/bin/env python3
"""Collect longitudinal monthly panel data by cloning repos and mining git history.

Reads the repo list from data/ai_adoption_repos.csv (output of the cross-
sectional collection) and produces three panel CSVs covering 2024-01 through
2026-03 (27 months):

  1. Monthly commit counts (outcome variable)
  2. Monthly active contributors (time-varying confounder)
  3. Treatment timing — first commit that introduced an L2+ AI config file

Each repo is cloned as a bare blobless clone (commits + trees, no file
content), so disk usage is ~50 GB for 1,000 repos.

Usage:
  # Full run with 8 parallel workers (default)
  python scripts/collect_ai_adoption_panel.py

  # Fewer workers / custom clone directory
  python scripts/collect_ai_adoption_panel.py --workers 4 --clone-dir /scratch/repos

Output:
  data/ai_adoption_panel_commits.csv
  data/ai_adoption_panel_contributors.csv
  data/ai_adoption_treatment_timing.csv
  data/ai_adoption_panel.csv              — merged analysis-ready panel
"""

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

from log_utils import setup_logging

log = setup_logging()

# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
REPOS_CSV = os.path.join(DATA_DIR, "ai_adoption_repos.csv")

COMMITS_CSV = os.path.join(DATA_DIR, "ai_adoption_panel_commits.csv")
CONTRIBUTORS_CSV = os.path.join(DATA_DIR, "ai_adoption_panel_contributors.csv")
TREATMENT_CSV = os.path.join(DATA_DIR, "ai_adoption_treatment_timing.csv")
PANEL_CSV = os.path.join(DATA_DIR, "ai_adoption_panel.csv")

DEFAULT_CLONE_DIR = os.path.join(PROJECT_ROOT, "repos_bare")

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


def clone_repo(full_name: str, clone_dir: str) -> bool:
    """Bare blobless clone from GitHub.  Returns True on success."""
    url = f"https://github.com/{full_name}.git"
    try:
        subprocess.run(
            ["git", "clone", "--filter=blob:none", "--bare", url, clone_dir],
            capture_output=True, text=True, timeout=600, check=True,
        )
        return True
    except subprocess.TimeoutExpired:
        log.warning("Clone timed out for %s", full_name)
        return False
    except subprocess.CalledProcessError as e:
        log.warning("Clone failed for %s: %s", full_name, e.stderr[:200] if e.stderr else e)
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


def process_repo(
    full_name: str, clone_base: str,
) -> tuple[str, list[dict], list[dict], dict]:
    """Clone (if needed) and extract all panel variables for one repo.

    Returns ``(full_name, commit_rows, contributor_rows, treatment_row)``.
    """
    safe_name = full_name.replace("/", "__")
    clone_dir = os.path.join(clone_base, safe_name + ".git")

    # Clone if not already present (allows resume without re-downloading)
    if not os.path.isdir(clone_dir):
        if not clone_repo(full_name, clone_dir):
            empty_treatment = {
                "full_name": full_name,
                "treatment_date": "",
                "treatment_month": "",
                "first_ai_file": "",
            }
            return full_name, [], [], empty_treatment

    # Monthly commits + contributors
    monthly = extract_monthly_data(clone_dir)
    commit_rows = []
    contrib_rows = []
    for m in SORTED_MONTHS:
        data = monthly.get(m, {"commits": 0, "active_contributors": 0})
        commit_rows.append({
            "full_name": full_name,
            "month": m,
            "commits": data["commits"],
        })
        contrib_rows.append({
            "full_name": full_name,
            "month": m,
            "active_contributors": data["active_contributors"],
        })

    # Treatment timing
    treatment = extract_treatment_timing(clone_dir)
    treatment["full_name"] = full_name

    return full_name, commit_rows, contrib_rows, treatment


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


# ── Panel assembly ───────────────────────────────────────────────────────────


def assemble_panel():
    """Merge commits, contributors, and treatment timing into one panel CSV.

    Joins on (full_name, month), adds treatment status and event-time
    variables, and attaches time-invariant repo covariates from the
    cross-sectional dataset.
    """
    log.info("Assembling merged panel …")

    commits = pd.read_csv(COMMITS_CSV)
    contribs = pd.read_csv(CONTRIBUTORS_CSV)
    treatment = pd.read_csv(TREATMENT_CSV)

    # Start from commits (one row per repo-month), merge contributors
    panel = commits.merge(contribs, on=["full_name", "month"], how="left")
    panel["active_contributors"] = (
        panel["active_contributors"].fillna(0).astype(int)
    )

    # Merge treatment timing (one row per repo → broadcast to all months)
    panel = panel.merge(
        treatment[["full_name", "treatment_date", "treatment_month",
                    "first_ai_file"]],
        on="full_name", how="left",
    )

    # Construct panel variables
    panel["treated"] = (
        panel["treatment_month"].notna()
        & (panel["month"] >= panel["treatment_month"])
    ).astype(int)

    # Event-time: months since treatment (negative = pre, 0 = onset month)
    def _months_between(row):
        if pd.isna(row["treatment_month"]) or row["treatment_month"] == "":
            return None
        ty, tm = map(int, row["treatment_month"].split("-"))
        my, mm = map(int, row["month"].split("-"))
        return (my - ty) * 12 + (mm - tm)

    panel["months_since_treatment"] = panel.apply(_months_between, axis=1)

    # Attach time-invariant covariates from cross-sectional data
    if os.path.exists(REPOS_CSV):
        repo_covs = pd.read_csv(REPOS_CSV)
        # Keep only columns that are plausibly time-invariant
        keep_cols = [
            "full_name", "owner_type", "queried_language", "primary_language",
            "created_at", "license", "ai_maturity_level",
        ]
        keep_cols = [c for c in keep_cols if c in repo_covs.columns]
        panel = panel.merge(repo_covs[keep_cols], on="full_name", how="left")

    panel.sort_values(["full_name", "month"], inplace=True)
    panel.to_csv(PANEL_CSV, index=False)

    n_repos = panel["full_name"].nunique()
    n_months = panel["month"].nunique()
    n_treated = panel.loc[panel["treated"] == 1, "full_name"].nunique()
    log.info(
        "Panel saved to %s  (%d repos × %d months = %d rows, %d ever-treated)",
        PANEL_CSV, n_repos, n_months, len(panel), n_treated,
    )


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

    repos_df = pd.read_csv(REPOS_CSV, usecols=["full_name"])
    all_repos = repos_df["full_name"].tolist()
    log.info("Loaded %d repos from %s", len(all_repos), REPOS_CSV)

    # ── Resume ───────────────────────────────────────────────────────────────
    processed = load_processed_repos(TREATMENT_CSV)
    if processed:
        log.info("Resuming: %d repos already processed", len(processed))

    remaining = [r for r in all_repos if r not in processed]
    log.info("Repos to process: %d", len(remaining))

    if not remaining:
        log.info("All repos already processed — assembling panel")
        assemble_panel()
        return

    # ── Prepare output ───────────────────────────────────────────────────────
    os.makedirs(args.clone_dir, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    commit_fields = ["full_name", "month", "commits"]
    contrib_fields = ["full_name", "month", "active_contributors"]
    treatment_fields = ["full_name", "treatment_date", "treatment_month",
                        "first_ai_file"]

    if not processed:
        pd.DataFrame(columns=commit_fields).to_csv(COMMITS_CSV, index=False)
        pd.DataFrame(columns=contrib_fields).to_csv(CONTRIBUTORS_CSV, index=False)
        pd.DataFrame(columns=treatment_fields).to_csv(TREATMENT_CSV, index=False)

    # ── Process repos ────────────────────────────────────────────────────────
    completed = len(processed)
    failed = 0

    commit_buf: list[dict] = []
    contrib_buf: list[dict] = []
    treatment_buf: list[dict] = []

    def flush():
        nonlocal commit_buf, contrib_buf, treatment_buf
        if commit_buf:
            pd.DataFrame(commit_buf).to_csv(
                COMMITS_CSV, mode="a", header=False, index=False)
            commit_buf = []
        if contrib_buf:
            pd.DataFrame(contrib_buf).to_csv(
                CONTRIBUTORS_CSV, mode="a", header=False, index=False)
            contrib_buf = []
        if treatment_buf:
            pd.DataFrame(treatment_buf).to_csv(
                TREATMENT_CSV, mode="a", header=False, index=False)
            treatment_buf = []

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(process_repo, repo, args.clone_dir): repo
                for repo in remaining
            }
            for future in as_completed(futures):
                repo = futures[future]
                try:
                    full_name, c_rows, ct_rows, t_row = future.result()
                except Exception:
                    log.exception("Unhandled error for %s", repo)
                    failed += 1
                    treatment_buf.append({
                        "full_name": repo,
                        "treatment_date": "",
                        "treatment_month": "",
                        "first_ai_file": "",
                    })
                    if len(treatment_buf) >= 10:
                        flush()
                    continue

                if not c_rows:
                    log.warning("No data for %s (clone may have failed)", full_name)
                    failed += 1
                else:
                    commit_buf.extend(c_rows)
                    contrib_buf.extend(ct_rows)

                treatment_buf.append(t_row)
                completed += 1

                total_commits = sum(r["commits"] for r in c_rows) if c_rows else 0
                log.info(
                    "[%d/%d] %s  commits=%d  treated=%s",
                    completed, len(all_repos), full_name, total_commits,
                    t_row.get("treatment_month") or "never",
                )

                if len(treatment_buf) >= 10:
                    flush()

    except KeyboardInterrupt:
        log.info("Interrupted — flushing partial progress")
    finally:
        flush()

    log.info(
        "Done. %d processed (%d failed). Output:\n  %s\n  %s\n  %s",
        completed, failed, COMMITS_CSV, CONTRIBUTORS_CSV, TREATMENT_CSV,
    )

    assemble_panel()


if __name__ == "__main__":
    main()
