#!/usr/bin/env python3
"""Fetch all papers citing Ray et al. (FSE 2014 / CACM 2017) from Semantic Scholar.

Queries the Semantic Scholar API for citing papers of both versions,
deduplicates by S2 paper ID, and writes the results to a CSV.

Usage:
    python scripts/fetch_ray_citations.py

Output:
    data/ray_citations.csv
"""

import csv
import json
import os
import sys
import time

import requests

from log_utils import setup_logging

log = setup_logging()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "ray_citations.csv")

# Semantic Scholar paper IDs for Ray et al.
PAPERS = {
    "FSE2014": {
        "s2_id": "346e2d94b09144375e2449cf214ac34ba93bb48c",
        "doi": "10.1145/2635868.2635922",
    },
    "CACM2017": {
        "s2_id": "a29876e47583ef978ea415c17a67493028f8831d",
        "doi": "10.1145/3126905",
    },
}

S2_API = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,citationCount,contexts,intents,externalIds,year,authors"
LIMIT = 1000
DELAY = 1.5  # seconds between API calls
MAX_RETRIES = 5


def fetch_citations(paper_id: str, version_label: str) -> list[dict]:
    """Fetch all citing papers for a given S2 paper ID."""
    url = f"{S2_API}/paper/{paper_id}/citations"
    all_citations = []
    offset = 0

    while True:
        params = {"fields": FIELDS, "limit": LIMIT, "offset": offset}

        for attempt in range(MAX_RETRIES):
            try:
                resp = requests.get(url, params=params, timeout=60)
                if resp.status_code == 200:
                    break
                if resp.status_code == 429:
                    wait = min(2 ** (attempt + 2), 60)
                    log.warning("  Rate limited, waiting %ds...", wait)
                    time.sleep(wait)
                    continue
                log.warning("  HTTP %d on attempt %d", resp.status_code, attempt + 1)
            except requests.RequestException as e:
                log.warning("  Request error on attempt %d: %s", attempt + 1, e)
            wait = min(2 ** (attempt + 1), 30)
            time.sleep(wait)
        else:
            log.error("  Failed after %d retries for %s offset=%d",
                      MAX_RETRIES, version_label, offset)
            break

        data = resp.json()
        batch = data.get("data", [])
        if not batch:
            break

        for item in batch:
            citing = item.get("citingPaper", {})
            citing["_cited_version"] = version_label
            # contexts and intents live on the citation edge, not inside citingPaper
            citing["_contexts"] = item.get("contexts") or []
            citing["_intents"] = item.get("intents") or []
            all_citations.append(citing)

        log.info("  %s: fetched %d citations (offset=%d)",
                 version_label, len(batch), offset)

        offset += len(batch)
        if offset >= data.get("total", 0) or len(batch) < LIMIT:
            break

        time.sleep(DELAY)

    return all_citations


def extract_external_id(external_ids: list[dict] | None, id_type: str) -> str:
    """Extract a specific external ID from S2 externalIds list."""
    if not external_ids:
        return ""
    for eid in external_ids:
        if isinstance(eid, dict) and eid.get("source") == id_type:
            return eid.get("value", "")
    # Sometimes externalIds is a dict, not a list
    if isinstance(external_ids, dict):
        return external_ids.get(id_type, "") or ""
    return ""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Fetch citations for both versions
    all_raw = []
    for label, info in PAPERS.items():
        log.info("Fetching citations for %s (S2 ID: %s)", label, info["s2_id"])
        citations = fetch_citations(info["s2_id"], label)
        log.info("  -> %d citations for %s", len(citations), label)
        all_raw.extend(citations)
        time.sleep(DELAY)

    # Deduplicate by S2 paper ID
    seen: dict[str, dict] = {}
    for paper in all_raw:
        pid = paper.get("paperId")
        if not pid:
            continue
        if pid in seen:
            # Paper cites both versions — merge contexts
            existing_version = seen[pid]["cited_version"]
            if existing_version != "both":
                seen[pid]["cited_version"] = "both"
            # Merge any additional contexts from the second version
            existing_ctx = json.loads(seen[pid]["contexts"])
            new_ctx = paper.get("_contexts") or []
            merged = existing_ctx + [c for c in new_ctx if c not in existing_ctx]
            seen[pid]["contexts"] = json.dumps(merged)
        else:
            authors_list = paper.get("authors") or []
            author_names = "; ".join(
                a.get("name", "") for a in authors_list if isinstance(a, dict)
            )
            ext_ids = paper.get("externalIds")
            doi = extract_external_id(ext_ids, "DOI")
            arxiv_id = extract_external_id(ext_ids, "ArXiv")
            # Handle dict-style externalIds
            if isinstance(ext_ids, dict):
                doi = ext_ids.get("DOI", "") or ""
                arxiv_id = ext_ids.get("ArXiv", "") or ""

            contexts = paper.get("_contexts") or []
            intents = paper.get("_intents") or []

            seen[pid] = {
                "s2_paper_id": pid,
                "title": paper.get("title", ""),
                "authors": author_names,
                "year": paper.get("year", ""),
                "cited_version": paper.get("_cited_version", ""),
                "citation_count": paper.get("citationCount", 0),
                "contexts": json.dumps(contexts),
                "intents": json.dumps(intents),
                "doi": doi,
                "arxiv_id": arxiv_id,
            }

    papers = sorted(seen.values(), key=lambda p: (p.get("year") or 0, p.get("title", "")))

    # Write CSV
    fieldnames = [
        "s2_paper_id", "title", "authors", "year", "cited_version",
        "citation_count", "contexts", "intents", "doi", "arxiv_id",
    ]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)

    # Summary stats
    total = len(papers)
    with_contexts = sum(1 for p in papers if p["contexts"] != "[]")
    both_count = sum(1 for p in papers if p["cited_version"] == "both")
    log.info("=" * 60)
    log.info("Total unique citing papers: %d", total)
    log.info("  With citation contexts: %d (%.0f%%)",
             with_contexts, 100 * with_contexts / total if total else 0)
    log.info("  Citing both versions: %d", both_count)
    log.info("Output: %s", OUTPUT_FILE)


if __name__ == "__main__":
    main()
