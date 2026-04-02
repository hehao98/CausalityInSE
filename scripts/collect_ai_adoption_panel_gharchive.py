#!/usr/bin/env python3
"""Fill GHArchive confounder columns in the panel CSV via BigQuery.

Queries the public githubarchive dataset on BigQuery for the ~1,000 repos
in the panel, aggregating monthly counts of stars, issues opened, forks,
PRs merged, and releases.  The results are joined back into
data/ai_adoption_panel.csv, filling the previously empty columns:

  new_stars, new_issues, new_forks, prs_merged, new_releases

Prerequisites:
  1.  Authenticate with GCP: either set GOOGLE_APPLICATION_CREDENTIALS to a
      service account key, or run ``gcloud auth application-default login``.
  2.  data/ai_adoption_panel.csv must exist (from collect_ai_adoption_panel.py).

Usage:
  python scripts/collect_ai_adoption_panel_gharchive.py

  # Use a specific GCP project for billing
  python scripts/collect_ai_adoption_panel_gharchive.py --project my-gcp-project

  # Query only, save raw BigQuery results without updating the panel
  python scripts/collect_ai_adoption_panel_gharchive.py --query-only

Output:
  data/ai_adoption_panel_gharchive.csv  — raw BigQuery results (backup)
  data/ai_adoption_panel.csv            — updated in place
"""

import argparse
import os
import sys
import textwrap

from google.cloud import bigquery
import pandas as pd

from log_utils import setup_logging

log = setup_logging()

# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
REPOS_CSV = os.path.join(DATA_DIR, "ai_adoption_repos.csv")
PANEL_CSV = os.path.join(DATA_DIR, "ai_adoption_panel.csv")
GHARCHIVE_CSV = os.path.join(DATA_DIR, "ai_adoption_panel_gharchive.csv")

# GHArchive columns that this script fills
GHARCHIVE_COLS = ["new_stars", "new_issues", "new_forks", "prs_merged",
                  "new_releases"]

# ── BigQuery ─────────────────────────────────────────────────────────────────

# BigQuery has a query size limit (~1 MB).  With 1,000 repo names averaging
# ~30 chars each, the IN list is ~40 KB — well within the limit.  But we
# chunk the query into batches if the repo list ever grows.
BATCH_SIZE = 500  # repos per BigQuery query


def build_query(repo_names: list[str]) -> str:
    """Build the GHArchive aggregation query for a batch of repos."""
    quoted = ", ".join(f"'{name}'" for name in repo_names)
    return textwrap.dedent(f"""\
        SELECT
          repo.name AS full_name,
          FORMAT_TIMESTAMP('%Y-%m', created_at) AS month,
          COUNTIF(type = 'WatchEvent') AS new_stars,
          COUNTIF(type = 'IssuesEvent'
                  AND JSON_EXTRACT_SCALAR(payload, '$.action') = 'opened')
            AS new_issues,
          COUNTIF(type = 'ForkEvent') AS new_forks,
          COUNTIF(type = 'PullRequestEvent'
                  AND JSON_EXTRACT_SCALAR(payload, '$.action') = 'closed'
                  AND JSON_EXTRACT_SCALAR(payload,
                        '$.pull_request.merged') = 'true')
            AS prs_merged,
          COUNTIF(type = 'ReleaseEvent') AS new_releases
        FROM `githubarchive.day.*`
        WHERE
          _TABLE_SUFFIX BETWEEN '20240101' AND '20260331'
          AND repo.name IN ({quoted})
          AND type IN ('WatchEvent', 'IssuesEvent', 'ForkEvent',
                       'PullRequestEvent', 'ReleaseEvent')
        GROUP BY full_name, month
        ORDER BY full_name, month
    """)


def run_bigquery(repo_names: list[str], project: str | None) -> pd.DataFrame:
    """Execute the GHArchive query on BigQuery, returning a DataFrame."""
    client = bigquery.Client(project=project)

    frames = []
    for i in range(0, len(repo_names), BATCH_SIZE):
        batch = repo_names[i : i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(repo_names) + BATCH_SIZE - 1) // BATCH_SIZE
        log.info("Running BigQuery batch %d/%d (%d repos)",
                 batch_num, total_batches, len(batch))

        query = build_query(batch)
        job = client.query(query)
        df = job.to_dataframe()

        bytes_billed = job.total_bytes_billed or 0
        log.info("  Batch %d done: %d rows, %.2f GB billed",
                 batch_num, len(df), bytes_billed / 1e9)
        frames.append(df)

    if not frames:
        return pd.DataFrame(columns=["full_name", "month"] + GHARCHIVE_COLS)

    result = pd.concat(frames, ignore_index=True)

    total_billed_tb = sum(
        (f.attrs.get("bytes_billed", 0) for f in frames), 0
    ) / 1e12
    log.info("BigQuery total: %d rows across %d repos",
             len(result), result["full_name"].nunique())

    return result


# ── Panel update ─────────────────────────────────────────────────────────────


def update_panel(gharchive_df: pd.DataFrame):
    """Join BigQuery results into the existing panel CSV."""
    if not os.path.exists(PANEL_CSV):
        log.error("Panel CSV not found: %s", PANEL_CSV)
        sys.exit(1)

    panel = pd.read_csv(PANEL_CSV, dtype=str)
    log.info("Loaded panel: %d rows", len(panel))

    # Drop old GHArchive columns (they were empty placeholders)
    panel.drop(columns=GHARCHIVE_COLS, errors="ignore", inplace=True)

    # Ensure BigQuery result types
    gha = gharchive_df.copy()
    for col in GHARCHIVE_COLS:
        if col in gha.columns:
            gha[col] = gha[col].astype(int)

    # Left-join on (full_name, month)
    panel = panel.merge(
        gha[["full_name", "month"] + GHARCHIVE_COLS],
        on=["full_name", "month"],
        how="left",
    )

    # Repos/months with no GHArchive events get 0 (not NaN)
    for col in GHARCHIVE_COLS:
        panel[col] = panel[col].fillna(0).astype(int)

    panel.to_csv(PANEL_CSV, index=False)

    coverage = panel[GHARCHIVE_COLS].sum().to_dict()
    log.info("Panel updated: %s", PANEL_CSV)
    log.info("  Column totals: %s",
             ", ".join(f"{k}={v}" for k, v in coverage.items()))


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--project", type=str, default=None,
        help="GCP project ID for BigQuery billing (uses default if omitted)",
    )
    parser.add_argument(
        "--query-only", action="store_true",
        help="Save raw BigQuery results to CSV without updating the panel",
    )
    args = parser.parse_args()

    # Load repo list
    if not os.path.exists(REPOS_CSV):
        log.error("Repo list not found: %s", REPOS_CSV)
        sys.exit(1)

    repos_df = pd.read_csv(REPOS_CSV, usecols=["full_name"])
    repo_names = repos_df["full_name"].tolist()
    log.info("Loaded %d repos", len(repo_names))

    # Check for existing BigQuery results (skip re-querying if present)
    if os.path.exists(GHARCHIVE_CSV):
        log.info("Found existing %s — loading instead of re-querying",
                 GHARCHIVE_CSV)
        gha_df = pd.read_csv(GHARCHIVE_CSV)
        log.info("  %d rows, %d repos",
                 len(gha_df), gha_df["full_name"].nunique())
    else:
        gha_df = run_bigquery(repo_names, args.project)
        gha_df.to_csv(GHARCHIVE_CSV, index=False)
        log.info("Raw results saved to %s", GHARCHIVE_CSV)

    if args.query_only:
        log.info("--query-only: skipping panel update")
        return

    update_panel(gha_df)


if __name__ == "__main__":
    main()
