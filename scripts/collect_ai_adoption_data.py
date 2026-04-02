#!/usr/bin/env python3
"""Collect cross-sectional data on AI coding tool adoption across top GitHub repos.

Phase 1 of the AI adoption worked example.  For each of 10 popular programming
languages, fetch the top N repositories by star count, collect repo-level
covariates, classify AI maturity level (L1--L4) by scanning the file tree for
known AI tool configuration files, detect AI bot contributors, and compute
monthly commit counts over a 6-month window.

Usage:
  # Test run: 10 repos per language (100 total)
  python scripts/collect_ai_adoption_data.py --per-language 10

  # Full run: 100 repos per language (1000 total)
  python scripts/collect_ai_adoption_data.py --per-language 100

Environment:
  Reads GITHUB_TOKEN from .env file in the project root.

Output:
  data/ai_adoption_repos.csv          — one row per repo (covariates + treatment)
  data/ai_adoption_monthly_commits.csv — one row per repo-month (outcome)
"""

import argparse
import csv
import os
import re
import sys
import time
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

import requests
from dotenv import load_dotenv

from log_utils import setup_logging

log = setup_logging()

# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
if not GITHUB_TOKEN:
    log.error("GITHUB_TOKEN not found in .env — aborting")
    sys.exit(1)

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data")
REPOS_CSV = os.path.join(OUTPUT_DIR, "ai_adoption_repos.csv")
MONTHLY_CSV = os.path.join(OUTPUT_DIR, "ai_adoption_monthly_commits.csv")

# ── Constants ────────────────────────────────────────────────────────────────

LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java",
    "C++", "C", "Go", "Rust", "Ruby", "Swift",
]

# 6-month outcome window ending at the start of the current month
WINDOW_END = datetime.now(timezone.utc).replace(
    day=1, hour=0, minute=0, second=0, microsecond=0,
)
WINDOW_START = WINDOW_END - relativedelta(months=6)
OUTCOME_MONTHS = []
cursor = WINDOW_START
while cursor < WINDOW_END:
    next_month = cursor + relativedelta(months=1)
    OUTCOME_MONTHS.append((cursor, next_month))
    cursor = next_month

# AI bot login patterns (case-insensitive substring match on contributor login)
AI_BOT_LOGINS = [
    "claude-ai", "anthropic", "devin-ai", "sweep-ai",
    "coderabbit", "copilot", "codex", "aider",
    "cursor-bot", "sourcegraph-bot",
]

# ── AI maturity classification (file-path patterns) ─────────────────────────

L4_PATTERNS = [
    r"^\.claude/agents/",
    r"^\.claude/handoffs/",
    r"^\.docker/mounts/\.claude/",
    r"^\.github/actions/write-claude-execution-report/",
    r"^mcp-docker\.json$",
    r"^mcp-local\.json$",
]

L3_PATTERNS = [
    r"^\.claude/commands/",
    r"^\.claude/skills/",
    r"^\.claude/workflows/",
    r"^\.claude/plan-.*\.md$",
    r"^\.github/.+/prompts/",
    r"^\.github/ai-triaging/",
    r"^\.github/claude-docs-auditor/",
    r"^\.github/admin-link-enrichment/prompts/",
]

L2_PATTERNS = [
    r"^CLAUDE\.md$",
    r"^\.claude/settings\.json$",
    r"^\.claude/settings\.local\.json$",
    r"^\.claude/architecture\.md$",
    r"^\.claude/rules/",
    r"^\.claude/knowledge/",
    r"^\.claude/archive/",
    r"^\.claude/output-styles/",
    r"^\.cursorrules$",
    r"^(.+/)?\.cursor/rules/",
    r"^(.+/)?\.cursor/mcp\.json$",
    r"^\.github/copilot-instructions\.md$",
    r"^AGENTS\.md$",
    r"^\.mcp\.json$",
]

_L4_RE = [re.compile(p) for p in L4_PATTERNS]
_L3_RE = [re.compile(p) for p in L3_PATTERNS]
_L2_RE = [re.compile(p) for p in L2_PATTERNS]


def classify_path(path: str) -> int | None:
    """Return 4, 3, 2 if the path matches an AI artifact pattern, else None."""
    for pat in _L4_RE:
        if pat.match(path):
            return 4
    for pat in _L3_RE:
        if pat.match(path):
            return 3
    for pat in _L2_RE:
        if pat.match(path):
            return 2
    return None


def classify_repo_from_paths(paths: list[str]) -> tuple[int, list[str]]:
    """Return (maturity_level, list_of_matching_artifact_paths)."""
    max_level = 1
    artifacts = []
    for p in paths:
        lvl = classify_path(p)
        if lvl is not None:
            artifacts.append(p)
            max_level = max(max_level, lvl)
    return max_level, artifacts


# ── GitHub API helpers ───────────────────────────────────────────────────────

REST_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

GRAPHQL_URL = "https://api.github.com/graphql"
GRAPHQL_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}


def _sleep_until_reset(response: requests.Response, api_type: str):
    """Compute and execute the wait time from rate-limit headers."""
    # Prefer Retry-After (used by secondary rate limits), fall back to reset ts
    retry_after = response.headers.get("Retry-After")
    if retry_after:
        wait = int(retry_after) + 1
    else:
        reset_ts = int(response.headers.get("X-RateLimit-Reset", 0))
        wait = max(reset_ts - int(time.time()), 0) + 2
    log.warning("%s rate-limited, sleeping %ds", api_type, wait)
    time.sleep(wait)


def _check_rate_limit(response: requests.Response, api_type: str = "rest"):
    """Preemptively sleep if we're close to hitting the rate limit."""
    remaining = int(response.headers.get("X-RateLimit-Remaining", 999))
    if remaining < 10:
        reset_ts = int(response.headers.get("X-RateLimit-Reset", 0))
        wait = max(reset_ts - int(time.time()), 0) + 2
        log.warning("%s rate limit near (%d remaining), sleeping %ds",
                    api_type, remaining, wait)
        time.sleep(wait)


def _is_rate_limited(response: requests.Response) -> bool:
    """Detect both primary and secondary GitHub rate limits."""
    if response.status_code == 429:
        return True
    if response.status_code == 403:
        body = response.text.lower()
        if "rate limit" in body or "secondary" in body:
            return True
    return False


def rest_get(url: str, params: dict | None = None, max_retries: int = 5) -> dict | list:
    """GET from GitHub REST API with retry and rate-limit handling."""
    for attempt in range(max_retries):
        resp = requests.get(url, headers=REST_HEADERS, params=params, timeout=30)
        if resp.status_code == 200:
            _check_rate_limit(resp, "REST")
            return resp.json()
        if _is_rate_limited(resp):
            log.warning("REST rate-limited (%d) for %s (attempt %d/%d)",
                        resp.status_code, url, attempt + 1, max_retries)
            _sleep_until_reset(resp, "REST")
            continue
        if resp.status_code in (502, 503):
            time.sleep(2 ** attempt)
            continue
        log.error("REST %d for %s: %s", resp.status_code, url, resp.text[:200])
        return {}
    log.error("REST exhausted %d retries for %s", max_retries, url)
    return {}


def graphql_query(query: str, variables: dict | None = None, max_retries: int = 5) -> dict:
    """Execute a GitHub GraphQL query with retry and rate-limit handling."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    for attempt in range(max_retries):
        resp = requests.post(
            GRAPHQL_URL, headers=GRAPHQL_HEADERS, json=payload, timeout=30,
        )
        if resp.status_code == 200:
            _check_rate_limit(resp, "GraphQL")
            data = resp.json()
            if "errors" in data:
                log.warning("GraphQL errors: %s", data["errors"][:2])
            return data
        if _is_rate_limited(resp):
            log.warning("GraphQL rate-limited (%d) (attempt %d/%d)",
                        resp.status_code, attempt + 1, max_retries)
            _sleep_until_reset(resp, "GraphQL")
            continue
        if resp.status_code in (502, 503):
            time.sleep(2 ** attempt)
            continue
        log.error("GraphQL %d: %s", resp.status_code, resp.text[:300])
        return {}
    log.error("GraphQL exhausted %d retries", max_retries)
    return {}


# ── Step 1: Search for top repos per language ────────────────────────────────

def search_repos(language: str, per_language: int) -> list[dict]:
    """Fetch top repos by stars for a given language via the REST Search API.

    Returns a list of repo dicts (from the GitHub API response).
    The Search API returns at most 100 results per page, and 1000 total.
    """
    repos = []
    per_page = min(per_language, 100)
    pages_needed = (per_language + per_page - 1) // per_page
    for page in range(1, pages_needed + 1):
        log.info("Searching %s repos (page %d/%d)", language, page, pages_needed)
        data = rest_get(
            "https://api.github.com/search/repositories",
            params={
                "q": f"language:{language} fork:false archived:false",
                "sort": "stars",
                "order": "desc",
                "per_page": per_page,
                "page": page,
            },
        )
        items = data.get("items", [])
        if not items:
            break
        repos.extend(items)
        if len(items) < per_page:
            break
        # Search API has a stricter secondary rate limit (~30 req/min)
        time.sleep(2)
    return repos[:per_language]


# ── Step 2: GraphQL enrichment (commits, PRs, issues, monthly commits) ──────

# Build the monthly commit count fragments dynamically.
def _monthly_fragments() -> str:
    """Generate GraphQL aliases for monthly commit counts."""
    parts = []
    for i, (start, end) in enumerate(OUTCOME_MONTHS):
        alias = f"month{i}"
        since = start.strftime("%Y-%m-%dT%H:%M:%SZ")
        until = end.strftime("%Y-%m-%dT%H:%M:%SZ")
        parts.append(
            f'{alias}: history(since: "{since}", until: "{until}") {{ totalCount }}'
        )
    return "\n            ".join(parts)


ENRICH_QUERY = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    defaultBranchRef {
      target {
        ... on Commit {
          history {
            totalCount
          }
          MONTHLY_FRAGMENTS
        }
      }
    }
    pullRequests {
      totalCount
    }
    issues {
      totalCount
    }
    releases {
      totalCount
    }
    hasDiscussionsEnabled
    object(expression: "HEAD:.github/workflows") {
      ... on Tree {
        entries {
          name
        }
      }
    }
  }
}
""".replace("MONTHLY_FRAGMENTS", _monthly_fragments())


def enrich_repo(owner: str, name: str) -> dict:
    """Fetch extra covariates and monthly commits via GraphQL."""
    data = graphql_query(ENRICH_QUERY, {"owner": owner, "name": name})
    repo = (data.get("data") or {}).get("repository")
    if not repo:
        return {}

    branch_ref = repo.get("defaultBranchRef") or {}
    target = branch_ref.get("target") or {}

    result = {
        "total_commits": (target.get("history") or {}).get("totalCount", 0),
        "total_prs": (repo.get("pullRequests") or {}).get("totalCount", 0),
        "total_issues": (repo.get("issues") or {}).get("totalCount", 0),
        "total_releases": (repo.get("releases") or {}).get("totalCount", 0),
        "has_discussions": repo.get("hasDiscussionsEnabled", False),
        "has_ci": repo.get("object") is not None,
    }

    # Monthly commit counts
    for i, (start, _end) in enumerate(OUTCOME_MONTHS):
        alias = f"month{i}"
        month_data = target.get(alias) or {}
        month_key = start.strftime("%Y-%m")
        result[f"commits_{month_key}"] = month_data.get("totalCount", 0)

    return result


# ── Step 3: File tree scan for AI maturity ───────────────────────────────────

def get_file_tree(owner: str, name: str, default_branch: str) -> list[str]:
    """Fetch the full recursive file tree via the REST Trees API."""
    url = f"https://api.github.com/repos/{owner}/{name}/git/trees/{default_branch}"
    data = rest_get(url, params={"recursive": "1"})
    if not data or "tree" not in data:
        return []
    truncated = data.get("truncated", False)
    if truncated:
        log.warning("%s/%s file tree was truncated", owner, name)
    return [entry["path"] for entry in data["tree"] if entry.get("type") in ("blob", "tree")]


# ── Step 4: AI bot contributor detection ─────────────────────────────────────

def detect_ai_bots(owner: str, name: str) -> list[str]:
    """Check the contributor list for known AI bot accounts."""
    url = f"https://api.github.com/repos/{owner}/{name}/contributors"
    data = rest_get(url, params={"per_page": 100})
    if not isinstance(data, list):
        return []
    bots_found = []
    for contributor in data:
        login = (contributor.get("login") or "").lower()
        for pattern in AI_BOT_LOGINS:
            if pattern in login:
                bots_found.append(contributor.get("login", ""))
                break
    return bots_found


# ── Main pipeline ────────────────────────────────────────────────────────────

REPO_CSV_FIELDS = [
    "full_name", "owner", "name", "owner_type", "queried_language",
    "primary_language", "description",
    # Covariates from Search API
    "stars", "forks", "open_issues", "watchers", "size_kb",
    "created_at", "pushed_at", "license", "has_wiki",
    "topics",
    # Covariates from GraphQL
    "total_commits", "total_prs", "total_issues", "total_releases",
    "has_discussions", "has_ci",
    # Treatment variables
    "ai_maturity_level", "ai_artifacts", "ai_bot_contributors",
]


def extract_search_fields(repo: dict, queried_language: str) -> dict:
    """Extract covariate fields from a Search API repo object."""
    return {
        "full_name": repo.get("full_name", ""),
        "owner": repo.get("owner", {}).get("login", ""),
        "name": repo.get("name", ""),
        "owner_type": repo.get("owner", {}).get("type", ""),
        "queried_language": queried_language,
        "primary_language": repo.get("language", ""),
        "description": (repo.get("description") or "")[:500],
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "open_issues": repo.get("open_issues_count", 0),
        "watchers": repo.get("subscribers_count", 0),
        "size_kb": repo.get("size", 0),
        "created_at": repo.get("created_at", ""),
        "pushed_at": repo.get("pushed_at", ""),
        "license": (repo.get("license") or {}).get("spdx_id", ""),
        "has_wiki": repo.get("has_wiki", False),
        "topics": ";".join(repo.get("topics", [])),
    }


def process_repo(repo: dict, queried_language: str) -> tuple[dict, list[dict]]:
    """Process a single repo: extract covariates, classify AI maturity, get monthly commits.

    Returns (repo_row, monthly_rows).
    """
    owner = repo["owner"]["login"]
    name = repo["name"]
    default_branch = repo.get("default_branch", "main")
    full_name = f"{owner}/{name}"

    row = extract_search_fields(repo, queried_language)

    # GraphQL enrichment
    log.info("  Enriching %s via GraphQL", full_name)
    gql = enrich_repo(owner, name)
    row.update({
        "total_commits": gql.get("total_commits", ""),
        "total_prs": gql.get("total_prs", ""),
        "total_issues": gql.get("total_issues", ""),
        "total_releases": gql.get("total_releases", ""),
        "has_discussions": gql.get("has_discussions", ""),
        "has_ci": gql.get("has_ci", ""),
    })

    # File tree scan for AI maturity
    log.info("  Scanning file tree for %s", full_name)
    paths = get_file_tree(owner, name, default_branch)
    ai_level, ai_artifacts = classify_repo_from_paths(paths)
    row["ai_maturity_level"] = ai_level
    row["ai_artifacts"] = ";".join(ai_artifacts)

    # AI bot detection
    log.info("  Checking AI bot contributors for %s", full_name)
    bots = detect_ai_bots(owner, name)
    row["ai_bot_contributors"] = ";".join(bots)

    # Monthly commit rows
    monthly_rows = []
    for i, (start, _end) in enumerate(OUTCOME_MONTHS):
        month_key = start.strftime("%Y-%m")
        monthly_rows.append({
            "full_name": full_name,
            "month": month_key,
            "commits": gql.get(f"commits_{month_key}", 0),
        })

    return row, monthly_rows


def load_existing(csv_path: str) -> set[str]:
    """Load full_name values from an existing CSV for resume support."""
    if not os.path.exists(csv_path):
        return set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {r["full_name"] for r in reader if "full_name" in r}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--per-language", type=int, default=10,
        help="Number of repos to fetch per language (default: 10)",
    )
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Resume support: skip repos already collected
    existing = load_existing(REPOS_CSV)
    if existing:
        log.info("Resuming: %d repos already collected", len(existing))

    # Determine if we need to write headers
    repos_file_exists = os.path.exists(REPOS_CSV) and len(existing) > 0
    monthly_file_exists = os.path.exists(MONTHLY_CSV) and len(existing) > 0

    # Month columns for the repo CSV header
    month_cols = [f"commits_{s.strftime('%Y-%m')}" for s, _ in OUTCOME_MONTHS]
    repo_fields = REPO_CSV_FIELDS + month_cols

    repos_f = open(REPOS_CSV, "a", newline="", encoding="utf-8")
    repos_writer = csv.DictWriter(repos_f, fieldnames=repo_fields, extrasaction="ignore")
    if not repos_file_exists:
        repos_writer.writeheader()

    monthly_f = open(MONTHLY_CSV, "a", newline="", encoding="utf-8")
    monthly_writer = csv.DictWriter(monthly_f, fieldnames=["full_name", "month", "commits"])
    if not monthly_file_exists:
        monthly_writer.writeheader()

    seen_full_names = set(existing)
    total_collected = len(existing)
    total_skipped = 0

    try:
        for lang in LANGUAGES:
            log.info("=== Fetching top %d %s repos by stars ===", args.per_language, lang)
            repos = search_repos(lang, args.per_language)
            log.info("Search returned %d %s repos", len(repos), lang)

            for repo in repos:
                full_name = repo.get("full_name", "")

                # Dedup across languages
                if full_name in seen_full_names:
                    log.info("  Skipping %s (already collected)", full_name)
                    total_skipped += 1
                    continue
                seen_full_names.add(full_name)

                # Exclusion: archived (should be filtered by search, but double-check)
                if repo.get("archived", False):
                    log.info("  Skipping %s (archived)", full_name)
                    total_skipped += 1
                    continue

                row, monthly_rows = process_repo(repo, lang)

                # Also embed monthly counts in the repo row for convenience
                for mr in monthly_rows:
                    row[f"commits_{mr['month']}"] = mr["commits"]

                repos_writer.writerow(row)
                repos_f.flush()

                monthly_writer.writerows(monthly_rows)
                monthly_f.flush()

                total_collected += 1
                log.info("  ✓ %s  L%d  commits=%s  [%d collected, %d skipped]",
                         full_name, row["ai_maturity_level"],
                         row.get("total_commits", "?"),
                         total_collected, total_skipped)

    except KeyboardInterrupt:
        log.info("Interrupted — progress saved (%d repos collected)", total_collected)
    finally:
        repos_f.close()
        monthly_f.close()

    log.info("Done. %d repos collected, %d skipped. Output: %s, %s",
             total_collected, total_skipped, REPOS_CSV, MONTHLY_CSV)


if __name__ == "__main__":
    main()
