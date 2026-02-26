#!/usr/bin/env python3
"""Download ICSE/FSE/ASE paper metadata (2015-2025) from Semantic Scholar API.

Queries each venue+year individually (S2 year ranges don't work reliably
with venue filters), tries multiple venue name variants per conference,
and deduplicates by paper ID.

Output: data/se_papers_metadata.csv  (columns: venue, title, abstract)
"""

import os
import time

import pandas as pd
import requests

from log_utils import setup_logging

log = setup_logging()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "se_papers_metadata.csv")

S2_BULK_URL = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
S2_FIELDS = "title,abstract,venue,year,publicationVenue"

YEAR_MIN = 2015
YEAR_MAX = 2025

VENUE_CONFIG = {
    "ICSE": [
        "ICSE",
        "International Conference on Software Engineering",
    ],
    "FSE": [
        "ESEC/SIGSOFT FSE",
        "SIGSOFT FSE",
        "Proc. ACM Softw. Eng.",
    ],
    "ASE": [
        "ASE",
        "International Conference on Automated Software Engineering",
    ],
}

REQUEST_DELAY = 3.0
MAX_RETRIES = 5


def fetch_papers(venue_query, year, max_retries=MAX_RETRIES):
    """Fetch all papers for a single venue query and year via S2 bulk search."""
    params = {
        "query": "",
        "venue": venue_query,
        "year": str(year),
        "fields": S2_FIELDS,
    }

    all_papers = []
    token = None
    page = 0

    while True:
        req_params = dict(params)
        if token:
            req_params["token"] = token

        success = False
        for attempt in range(max_retries):
            try:
                resp = requests.get(S2_BULK_URL, params=req_params, timeout=60)

                if resp.status_code == 429:
                    wait = min(2 ** (attempt + 3), 120)
                    log.warning("Rate limited, waiting %ds …", wait)
                    time.sleep(wait)
                    continue

                resp.raise_for_status()
                success = True
                break

            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    log.error("Failed after %d retries: %s", max_retries, e)
                    return all_papers
                wait = 5 * (attempt + 1)
                log.warning("Retry %d/%d in %ds: %s", attempt + 1, max_retries, wait, e)
                time.sleep(wait)

        if not success:
            break

        data = resp.json()
        papers = data.get("data", [])
        all_papers.extend(papers)
        page += 1

        token = data.get("token")
        if not token or not papers:
            break

        time.sleep(REQUEST_DELAY)

    return all_papers


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_rows = []
    seen_ids = set()

    for venue_label, venue_queries in VENUE_CONFIG.items():
        log.info("%s", "=" * 60)
        log.info("  %s  (%d-%d)", venue_label, YEAR_MIN, YEAR_MAX)
        log.info("%s", "=" * 60)

        for year in range(YEAR_MIN, YEAR_MAX + 1):
            year_added = 0

            for vq in venue_queries:
                papers = fetch_papers(vq, year)

                added = 0
                for p in papers:
                    pid = p.get("paperId")
                    if not pid or pid in seen_ids:
                        continue
                    seen_ids.add(pid)

                    title = (p.get("title") or "").strip()
                    abstract = (p.get("abstract") or "").strip()
                    p_year = p.get("year")

                    if not title or not p_year:
                        continue
                    if p_year < YEAR_MIN or p_year > YEAR_MAX:
                        continue

                    all_rows.append({
                        "venue": f"{venue_label} {p_year}",
                        "title": title,
                        "abstract": abstract,
                    })
                    added += 1

                year_added += added
                time.sleep(REQUEST_DELAY)

            status = "OK" if year_added > 0 else "MISSING"
            log.info("  %s %d: %4d papers  [%s]", venue_label, year, year_added, status)

    df = pd.DataFrame(all_rows, columns=["venue", "title", "abstract"])
    df.sort_values("venue", inplace=True)
    df.to_csv(OUTPUT_FILE, index=False)

    log.info("%s", "=" * 60)
    log.info("  Summary")
    log.info("%s", "=" * 60)
    venue_counts = df["venue"].value_counts().sort_index()
    for venue, count in venue_counts.items():
        log.info("  %s: %4d papers", venue, count)
    log.info("  Total: %d papers", len(df))
    log.info("  Saved to %s", OUTPUT_FILE)


if __name__ == "__main__":
    main()
