#!/usr/bin/env python3
"""Download main-track ICSE/FSE/ASE paper metadata and PDFs (2015-2025).

Pipeline:
  1. Fetch paper lists from DBLP proceedings pages (XML) — main research
     track only (excludes companion, workshop, and satellite volumes).
  2. Batch-query Semantic Scholar for abstracts using DOIs.
  3. Backfill remaining missing abstracts via the OpenAlex API.
  4. Optionally download PDFs from IEEE Xplore / ACM Digital Library.
  5. Write venue, title, abstract, doi to CSV.

Proceedings mapping:
  ICSE  2015      → conf/icse/icse2015-1  (Volume 1 = research track)
  ICSE  2016-2025 → conf/icse/icse{year}
  FSE   2015-2023 → conf/sigsoft/fse{year}
  FSE   2024      → journals/pacmse/pacmse1  (journal-first, all FSE)
  FSE   2025      → journals/pacmse/pacmse2  (filter <number>FSE</number>)
  ASE   2015-2025 → conf/kbse/ase{year}

Usage:
  python scripts/download_papers.py               # metadata only
  python scripts/download_papers.py --pdfs         # metadata + PDF download

Output:
  data/se_papers_metadata.csv
  data/pdfs/*.pdf  (when --pdfs is given)
"""

import argparse
import csv
import json
import os
import re
import time
from collections import Counter
from pathlib import Path

import requests

from log_utils import setup_logging

log = setup_logging()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "se_papers_metadata.csv")
PDF_DIR = os.path.join(OUTPUT_DIR, "pdfs")

DBLP_BASE = "https://dblp.org/db"
S2_BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
S2_BATCH_SIZE = 400
S2_FIELDS = "title,abstract"

OPENALEX_WORKS_URL = "https://api.openalex.org/works"
OPENALEX_BATCH_SIZE = 50
OPENALEX_HEADERS = {"User-Agent": "CausalitySE/1.0 (mailto:research@cmu.edu)"}

YEAR_MIN = 2015
YEAR_MAX = 2025

MAX_RETRIES = 8
DBLP_DELAY = 1.0
S2_DELAY = 3.0
PDF_DELAY = 3.0

BROWSER_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# DBLP helpers
# ---------------------------------------------------------------------------

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
    """Extract paper title and DOI from DBLP XML."""
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

# ---------------------------------------------------------------------------
# Semantic Scholar abstracts
# ---------------------------------------------------------------------------

def fetch_abstracts_s2(dois: list[str]) -> dict[str, str]:
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

# ---------------------------------------------------------------------------
# OpenAlex abstract backfill
# ---------------------------------------------------------------------------

def _reconstruct_abstract(inverted_index: dict) -> str:
    """Rebuild plain text from an OpenAlex inverted-index abstract."""
    positions: dict[int, str] = {}
    for word, idxs in inverted_index.items():
        for i in idxs:
            positions[i] = word
    return " ".join(positions[i] for i in sorted(positions))


def fetch_abstracts_openalex(dois: list[str]) -> dict[str, str]:
    """Query OpenAlex for abstracts of papers identified by DOI.

    Uses the filter API to batch multiple DOIs per request (up to 50).
    """
    result: dict[str, str] = {}
    if not dois:
        return result

    for i in range(0, len(dois), OPENALEX_BATCH_SIZE):
        batch = dois[i : i + OPENALEX_BATCH_SIZE]
        doi_filter = "|".join(f"https://doi.org/{d}" for d in batch)

        for attempt in range(MAX_RETRIES):
            try:
                resp = requests.get(
                    OPENALEX_WORKS_URL,
                    params={
                        "filter": f"doi:{doi_filter}",
                        "per_page": str(len(batch)),
                        "select": "doi,abstract_inverted_index",
                    },
                    headers=OPENALEX_HEADERS,
                    timeout=60,
                )
                if resp.status_code == 429:
                    wait = min(2 ** (attempt + 2), 60)
                    log.warning("  OpenAlex rate-limited, waiting %ds", wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                break
            except requests.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    log.error("  OpenAlex batch failed: %s", e)
                    break
                time.sleep(3 * (attempt + 1))
        else:
            continue

        for work in resp.json().get("results", []):
            raw_doi = (work.get("doi") or "").replace("https://doi.org/", "")
            inv = work.get("abstract_inverted_index")
            if raw_doi and inv:
                result[raw_doi] = _reconstruct_abstract(inv)

        time.sleep(0.5)

    return result

# ---------------------------------------------------------------------------
# PDF download helpers
# ---------------------------------------------------------------------------

def _doi_to_filename(doi: str) -> str:
    """Sanitize a DOI into a safe PDF filename."""
    return doi.replace("/", "_") + ".pdf"


def _download_ieee_pdf(doi: str, session: requests.Session, dest: Path) -> bool:
    """Download a PDF from IEEE Xplore.

    Resolves the DOI to find the IEEE article number, then fetches the
    PDF via the stampPDF/getPDF.jsp endpoint.
    """
    try:
        page_resp = session.get(f"https://doi.org/{doi}", timeout=30, allow_redirects=True)
        page_resp.raise_for_status()
    except requests.RequestException as e:
        log.debug("  IEEE page fetch failed for %s: %s", doi, e)
        return False

    meta_match = re.search(
        r"xplGlobal\.document\.metadata\s*=\s*(\{.*?\});",
        page_resp.text,
        re.DOTALL,
    )
    arnumber = None
    if meta_match:
        try:
            arnumber = json.loads(meta_match.group(1)).get("arnumber")
        except json.JSONDecodeError:
            pass
    if not arnumber:
        m = re.search(r"/document/(\d+)", page_resp.url)
        arnumber = m.group(1) if m else None
    if not arnumber:
        log.debug("  IEEE arnumber not found for %s", doi)
        return False

    pdf_url = (
        f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp"
        f"?tp=&arnumber={arnumber}&ref="
    )
    try:
        pdf_resp = session.get(pdf_url, timeout=60, allow_redirects=True)
        pdf_resp.raise_for_status()
        if pdf_resp.content[:5] != b"%PDF-":
            log.debug("  IEEE response not PDF for %s", doi)
            return False
        dest.write_bytes(pdf_resp.content)
        return True
    except requests.RequestException as e:
        log.debug("  IEEE PDF download failed for %s: %s", doi, e)
        return False


def _download_acm_pdf(doi: str, session: requests.Session, dest: Path) -> bool:
    """Download a PDF from ACM Digital Library.

    Tries multiple strategies in order:
      1. cloudscraper  (Cloudflare JS-challenge solver)
      2. curl_cffi     (TLS-fingerprint impersonation)
      3. plain requests (works when on institutional network)
    """
    pdf_url = f"https://dl.acm.org/doi/pdf/{doi}"
    strategies: list[tuple[str, callable]] = []

    try:
        import cloudscraper
        _cs = cloudscraper.create_scraper()
        strategies.append(("cloudscraper", lambda: _cs.get(pdf_url, timeout=60)))
    except ImportError:
        pass

    try:
        from curl_cffi import requests as cffi_requests
        strategies.append((
            "curl_cffi",
            lambda: cffi_requests.get(pdf_url, impersonate="chrome", timeout=60, allow_redirects=True),
        ))
    except ImportError:
        pass

    strategies.append(("requests", lambda: session.get(pdf_url, timeout=60, allow_redirects=True)))

    for name, fetch in strategies:
        try:
            resp = fetch()
            if resp.status_code == 200 and resp.content[:5] == b"%PDF-":
                dest.write_bytes(resp.content)
                return True
        except Exception:
            pass

    log.debug("  ACM PDF failed (all strategies) for %s", doi)
    return False


def download_pdfs(rows: list[dict]) -> tuple[int, int, int]:
    """Download PDFs for all papers with DOIs.

    Returns (success_count, skip_count, fail_count).
    """
    os.makedirs(PDF_DIR, exist_ok=True)
    pdf_dir = Path(PDF_DIR)

    session = requests.Session()
    session.headers.update({"User-Agent": BROWSER_UA})

    success = skip = fail = 0
    total = sum(1 for r in rows if r.get("doi"))

    for idx, row in enumerate(rows):
        doi = row.get("doi")
        if not doi:
            continue

        dest = pdf_dir / _doi_to_filename(doi)
        if dest.exists():
            skip += 1
            continue

        is_ieee = doi.startswith("10.1109/")

        if is_ieee:
            ok = _download_ieee_pdf(doi, session, dest)
        else:
            ok = _download_acm_pdf(doi, session, dest)

        if ok:
            success += 1
            if success % 50 == 0:
                log.info("  PDF progress: %d downloaded, %d skipped, %d failed", success, skip, fail)
        else:
            fail += 1

        time.sleep(PDF_DELAY)

    return success, skip, fail

# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pdfs", action="store_true", help="Also download PDFs to data/pdfs/")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_rows: list[dict] = []

    # ---- Phase 1: paper lists from DBLP + S2 abstracts --------------------
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
            abstracts = fetch_abstracts_s2(dois)
            log.info("    Got %d abstracts from S2", len(abstracts))

            for p in papers:
                abstract = abstracts.get(p["doi"], "") if p["doi"] else ""
                all_rows.append({
                    "venue": f"{venue} {year}",
                    "title": p["title"],
                    "abstract": abstract,
                    "doi": p["doi"] or "",
                })

            time.sleep(DBLP_DELAY)

    # ---- Phase 2: backfill missing abstracts via OpenAlex -----------------
    missing_dois = [r["doi"] for r in all_rows if r["doi"] and not r["abstract"]]
    if missing_dois:
        log.info("%s", "=" * 60)
        log.info("  OpenAlex backfill: %d papers missing abstracts", len(missing_dois))
        log.info("%s", "=" * 60)
        oa_abstracts = fetch_abstracts_openalex(missing_dois)
        log.info("  Got %d abstracts from OpenAlex", len(oa_abstracts))
        filled = 0
        for row in all_rows:
            if not row["abstract"] and row["doi"] in oa_abstracts:
                row["abstract"] = oa_abstracts[row["doi"]]
                filled += 1
        log.info("  Filled %d additional abstracts", filled)

    # ---- Write CSV --------------------------------------------------------
    all_rows.sort(key=lambda r: r["venue"])

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["venue", "title", "abstract", "doi"])
        writer.writeheader()
        writer.writerows(all_rows)

    venue_counts = Counter(r["venue"] for r in all_rows)
    with_abstract = sum(1 for r in all_rows if r["abstract"])
    log.info("%s", "=" * 60)
    log.info("  Metadata summary")
    log.info("%s", "=" * 60)
    for v in sorted(venue_counts):
        print(f"  {v}: {venue_counts[v]:>4} papers")
    log.info("  Total: %d papers (%d with abstracts)", len(all_rows), with_abstract)
    log.info("  Saved to %s", OUTPUT_FILE)

    # ---- Phase 3: download PDFs -------------------------------------------
    if args.pdfs:
        log.info("%s", "=" * 60)
        log.info("  Downloading PDFs to %s", PDF_DIR)
        log.info("%s", "=" * 60)
        success, skip, fail = download_pdfs(all_rows)
        log.info(
            "  PDFs done: %d downloaded, %d already existed, %d failed",
            success, skip, fail,
        )


if __name__ == "__main__":
    main()
