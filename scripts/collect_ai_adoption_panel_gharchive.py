#!/usr/bin/env python3
"""Fill GHArchive confounder columns in the panel CSV via BigQuery.

Queries the public githubarchive dataset on BigQuery for the ~1,000 repos
in the panel, aggregating monthly counts of stars, issues opened, forks,
PRs merged, and releases.  The results are joined directly into
data/ai_adoption_panel.csv, filling the columns:

  new_stars, new_issues, new_forks, prs_merged, new_releases

Prerequisites:
  1.  Authenticate with GCP: either set GOOGLE_APPLICATION_CREDENTIALS to a
      service account key, or run ``gcloud auth application-default login``.
  2.  data/ai_adoption_panel.csv must exist (from collect_ai_adoption_panel.py).

Usage:
  python scripts/collect_ai_adoption_panel_gharchive.py

  # Use a specific GCP project for billing
  python scripts/collect_ai_adoption_panel_gharchive.py --project my-gcp-project

Output:
  data/ai_adoption_panel.csv  — updated in place
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
PANEL_CSV = os.path.join(DATA_DIR, "ai_adoption_panel.csv")

# GHArchive columns that this script fills
GHARCHIVE_COLS = ["new_stars", "new_issues", "new_forks", "prs_merged",
                  "new_releases"]

# ── BigQuery ─────────────────────────────────────────────────────────────────

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
        FROM `githubarchive.day.2*`
        WHERE
          _TABLE_SUFFIX BETWEEN '0240101' AND '0260331'
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
        # Avoid job.to_dataframe() which requires db-dtypes (incompatible
        # with pandas 3.x).  Fetch raw rows and build the DataFrame manually.
        rows = [dict(row) for row in job.result()]
        df = pd.DataFrame(rows, columns=["full_name", "month"] + GHARCHIVE_COLS)

        bytes_billed = job.total_bytes_billed or 0
        log.info("  Batch %d done: %d rows, %.2f GB billed",
                 batch_num, len(df), bytes_billed / 1e9)
        frames.append(df)

    if not frames:
        return pd.DataFrame(columns=["full_name", "month"] + GHARCHIVE_COLS)

    result = pd.concat(frames, ignore_index=True)
    log.info("BigQuery total: %d rows across %d repos",
             len(result), result["full_name"].nunique())

    return result


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
    args = parser.parse_args()

    # ── Load panel ───────────────────────────────────────────────────────────
    if not os.path.exists(PANEL_CSV):
        log.error("Panel CSV not found: %s", PANEL_CSV)
        sys.exit(1)

    panel = pd.read_csv(PANEL_CSV)
    log.info("Loaded panel: %d rows, %d repos",
             len(panel), panel["full_name"].nunique())

    # Check if GHArchive columns are already populated
    already_filled = all(
        col in panel.columns and panel[col].notna().any() and (panel[col] != 0).any()
        for col in GHARCHIVE_COLS
    )
    if already_filled:
        log.info("GHArchive columns already populated — nothing to do")
        return

    # ── Query BigQuery ───────────────────────────────────────────────────────
    repo_names = panel["full_name"].unique().tolist()
    gha = run_bigquery(repo_names, args.project)

    for col in GHARCHIVE_COLS:
        if col in gha.columns:
            gha[col] = gha[col].astype(int)

    # ── Update panel in place ────────────────────────────────────────────────
    panel.drop(columns=GHARCHIVE_COLS, errors="ignore", inplace=True)

    panel = panel.merge(
        gha[["full_name", "month"] + GHARCHIVE_COLS],
        on=["full_name", "month"],
        how="left",
    )

    for col in GHARCHIVE_COLS:
        panel[col] = panel[col].fillna(0).astype(int)

    panel.to_csv(PANEL_CSV, index=False)

    coverage = panel[GHARCHIVE_COLS].sum().to_dict()
    log.info("Panel updated: %s", PANEL_CSV)
    log.info("  Column totals: %s",
             ", ".join(f"{k}={v}" for k, v in coverage.items()))


if __name__ == "__main__":
    main()
