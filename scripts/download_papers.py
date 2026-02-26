#!/usr/bin/env python3
"""Download main-track ICSE/FSE/ASE paper metadata (2015-2025).

Strategy:
  1. Fetch paper lists from DBLP proceedings pages (XML) to restrict to
     the main research track — excludes companion, workshop, and satellite
     proceedings.
  2. Batch-query Semantic Scholar for abstracts using DOIs.
  3. Write venue, title, abstract to CSV.

Proceedings mapping:
  ICSE  2015      → conf/icse/icse2015-1  (Volume 1 = research track)
  ICSE  2016-2025 → conf/icse/icse{year}
  FSE   2015-2023 → conf/sigsoft/fse{year}
  FSE   2024      → journals/pacmse/pacmse1  (journal-first, all FSE)
  FSE   2025      → journals/pacmse/pacmse2  (filter <number>FSE</number>)
  ASE   2015-2025 → conf/kbse/ase{year}

Output: data/se_papers_metadata.csv
"""

import csv
import os
import re
import sys
import time
from collections import Counter

import requests

from log_utils import setup_logging

log = setup_logging()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "se_papers_metadata.csv")

DBLP_BASE = "https://dblp.org/db"
S2_BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
S2_BATCH_SIZE = 400
S2_FIELDS = "title,abstract"

YEAR_MIN = 2015
YEAR_MAX = 2025

MAX_RETRIES = 8
DBLP_DELAY = 1.0
S2_DELAY = 3.0


def _dblp_proceedings_path(venue: str, year: int) -> str:
    """Return the DBLP XML path (relative to DBLP_BASE) for the main proceedings."""
    if venue == "ICSE":
        key = "icse2015-1" if year == 2015 else f"icse{year}"
        return f"conf/icse/{key}.xml"
    if venue == "FSE":
        if year <= 2023:
            return f"conf/sigsoft/fse{year}.xml"
        if year == 2024:
            return "journals/pacmse/pacmse1.xml"
        return "journals/pacmse/pacmse2.xml"
    if venue == "ASE":
        return f"conf/kbse/ase{year}.xml"
    raise ValueError(f"Unknown venue: {venue}")


def fetch_dblp_page(url: str) -> str | None:
    """Fetch a DBLP page with retries."""
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200 and resp.text.strip():
                return resp.text
            if resp.status_code == 404:
                log.warning("  DBLP 404: %s", url)
                return None
        except requests.RequestException as e:
            log.warning("  DBLP attempt %d: %s", attempt + 1, e)
        wait = min(2 ** (attempt + 1), 30)
        time.sleep(wait)
    log.error("  DBLP failed after %d retries: %s", MAX_RETRIES, url)
    return None


def parse_dblp_entries(xml_text: str, venue: str, year: int) -> list[dict]:
    """Extract paper title and DOI from DBLP XML.

    For FSE 2025 (PACMSE Vol 2), only entries with <number>FSE</number>
    are included.
    """
    entries_inproc = re.findall(r"<inproceedings[^>]*>.*?</inproceedings>", xml_text, re.DOTALL)
    entries_article = re.findall(r"<article[^>]*>.*?</article>", xml_text, re.DOTALL)
    raw_entries = entries_inproc if entries_inproc else entries_article

    papers = []
    for entry in raw_entries:
        if venue == "FSE" and year == 2025:
            if "<number>FSE</number>" not in entry:
                continue

        title_m = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
        if not title_m:
            continue
        title = re.sub(r"\s+", " ", title_m.group(1)).strip().rstrip(".")

        doi = None
        for ee in re.findall(r"<ee[^>]*>(.*?)</ee>", entry):
            doi_m = re.search(r"doi\.org/(.+)", ee)
            if doi_m:
                doi = doi_m.group(1).strip()
                break

        papers.append({"title": title, "doi": doi})

    return papers


def fetch_abstracts_batch(dois: list[str]) -> dict[str, str]:
    """Batch-query Semantic Scholar for abstracts keyed by DOI."""
    result: dict[str, str] = {}
    ids = [f"DOI:{d}" for d in dois if d]
    if not ids:
        return result

    for i in range(0, len(ids), S2_BATCH_SIZE):
        batch = ids[i : i + S2_BATCH_SIZE]

        for attempt in range(MAX_RETRIES):
            try:
                resp = requests.post(
                    S2_BATCH_URL,
                    params={"fields": S2_FIELDS},
                    json={"ids": batch},
                    timeout=60,
                )
                if resp.status_code == 429:
                    wait = min(2 ** (attempt + 3), 120)
                    log.warning("  S2 rate-limited, waiting %ds", wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                break
            except requests.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    log.error("  S2 batch failed: %s", e)
                    break
                time.sleep(5 * (attempt + 1))
        else:
            continue

        for paper, doi_id in zip(resp.json(), batch):
            if paper is None:
                continue
            doi_key = doi_id.removeprefix("DOI:")
            abstract = (paper.get("abstract") or "").strip()
            if abstract:
                result[doi_key] = abstract

        time.sleep(S2_DELAY)

    return result


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_rows: list[dict] = []

    for venue in ("ICSE", "FSE", "ASE"):
        log.info("%s", "=" * 60)
        log.info("  %s  (%d–%d)", venue, YEAR_MIN, YEAR_MAX)
        log.info("%s", "=" * 60)

        for year in range(YEAR_MIN, YEAR_MAX + 1):
            path = _dblp_proceedings_path(venue, year)
            url = f"{DBLP_BASE}/{path}"

            xml = fetch_dblp_page(url)
            if not xml:
                log.warning("  %s %d: SKIPPED (page unavailable)", venue, year)
                continue

            papers = parse_dblp_entries(xml, venue, year)
            log.info("  %s %d: %d papers from DBLP", venue, year, len(papers))

            dois = [p["doi"] for p in papers if p["doi"]]
            log.info("    Fetching abstracts for %d papers with DOIs …", len(dois))
            abstracts = fetch_abstracts_batch(dois)
            log.info("    Got %d abstracts from S2", len(abstracts))

            for p in papers:
                abstract = abstracts.get(p["doi"], "") if p["doi"] else ""
                all_rows.append({
                    "venue": f"{venue} {year}",
                    "title": p["title"],
                    "abstract": abstract,
                })

            time.sleep(DBLP_DELAY)

    all_rows.sort(key=lambda r: r["venue"])

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["venue", "title", "abstract"])
        writer.writeheader()
        writer.writerows(all_rows)

    venue_counts = Counter(r["venue"] for r in all_rows)
    with_abstract = sum(1 for r in all_rows if r["abstract"])
    log.info("%s", "=" * 60)
    log.info("  Summary")
    log.info("%s", "=" * 60)
    for v in sorted(venue_counts):
        print(f"  {v}: {venue_counts[v]:>4} papers")
    log.info("  Total: %d papers (%d with abstracts)", len(all_rows), with_abstract)
    log.info("  Saved to %s", OUTPUT_FILE)


if __name__ == "__main__":
    main()
