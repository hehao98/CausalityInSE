# PL vs. Code Quality Literature Synthesis Plan

**Date:** 2026-03-27 (updated 2026-03-27)
**Scope:** Sections 4.1 (literature synthesis) and 4.2 (misinterpretation problem) of the unified Section 4.
**Goal:** Write a literature synthesis that (a) traces the PL vs. code quality debate as a coherent narrative, (b) documents the downstream misinterpretation problem with quantitative evidence, and (c) argues that the debate's impasse is about *identification*, setting up the two worked examples.

---

## Section 4.1: Literature Synthesis --- DONE

Section 4.1 has been expanded from ~20 lines to ~60 lines. Changes made:

- [x] Added Endrikat et al. (2014) to controlled experiments paragraph
- [x] Added Bhattacharya & Neamtiu (2011), Bissyandé et al. (2013), Kochhar et al. (2016) to observational studies paragraph
- [x] Key argument added: independent replication of an association is not the same as causal identification
- [x] Strengthened "toward causal identification" paragraph: Furia et al. (2024) finding described as "smoking gun" --- same data, same researchers, different conclusions depending on associational vs. causal analysis
- [x] Added section-level intro connecting to the umbrella theme
- [x] Three new BibTeX entries added to references.bib (DBLP:conf/icse/EndrikatHRS14, DBLP:conf/icse/BhattacharyaN11, DBLP:conf/compsac/BissyandeTLJR13)

---

## Section 4.2: The Misinterpretation Problem --- TODO

Two evidence streams converging on the same conclusion.

### Stream 1: Quantitative Citation Analysis of Ray et al.

#### Data Collection: `scripts/fetch_ray_citations.py`

Fetch ALL citing papers for both versions of the Ray et al. study from Semantic Scholar API into `data/ray_citations.csv`.

**Semantic Scholar details:**
- FSE 2014 paper (DOI: 10.1145/2635868.2635922): ~424 citations, S2 ID `346e2d94b09144375e2449cf214ac34ba93bb48c`
- CACM 2017 paper (DOI: 10.1145/3126905): ~36 citations, S2 ID `a29876e47583ef978ea415c17a67493028f8831d`
- The `contexts` field contains citation text snippets (the sentences/passages where the citation appears)
- Pagination: `offset`/`limit` params, max `limit=1000`
- Both paper versions must be queried separately (different S2 IDs, non-overlapping citation lists)
- Some papers will have empty `contexts` (no full-text access)

**Script behavior:**
1. Query `/paper/{id}/citations?fields=title,citationCount,contexts,intents,externalIds,year,authors&limit=1000` for both paper IDs
2. Deduplicate by S2 paper ID (a paper might cite both versions)
3. Output CSV with columns: `s2_paper_id`, `title`, `authors`, `year`, `cited_version` (FSE/CACM/both), `citation_count`, `contexts` (JSON array of text snippets), `doi`, `arxiv_id`
4. Add a 1-second delay between API calls to respect rate limits
5. Report total count and how many have non-empty contexts

**Expected output:** ~450--460 unique citing papers, of which roughly 50--70% will have citation context text.

#### Classification: `scripts/classify_ray_citations.py`

Read `data/ray_citations.csv`, classify each paper's citation interpretation, and write the classification back to the same CSV (adding new columns).

**Classification approach:**
1. For each citing paper with non-empty `contexts`, feed the citation text snippets to an LLM (Claude) and ask it to classify the interpretation
2. The **specific classification scheme should be determined after inspecting the actual citation text** --- run the fetch script first, manually examine 20--30 examples, then define categories that capture the natural variation
3. Likely categories (to be confirmed after data inspection):
   - *Causal*: Treats the finding as evidence that language features cause quality differences
   - *Associational/hedged*: Accurately describes the finding as a correlation or association
   - *Neutral/tangential*: Cites for context (dataset, motivation, related work) without interpreting findings
   - *Critical*: Cites to critique the methodology or question the findings
4. Papers with empty contexts get classified as `no_context`
5. Add columns: `classification`, `classification_confidence`, `representative_quote`

**Output:** Updated `data/ray_citations.csv` with classification columns. Summary statistics for the paper.

### Stream 2: Media and Practitioner Discourse Examples

The following examples have been collected for review. Each shows how Ray et al.'s hedged correlational findings were amplified into causal claims in practitioner contexts.

#### Example 1: The Register (2019) --- Debunking article with Berger quote

- **URL:** https://www.theregister.com/2019/01/30/programming_bugs/
- **Title:** "Boffins debunk study claiming certain languages lead to more buggy code"
- **Date:** January 30, 2019
- **Key quote (Emery Berger):** "The original study purported to establish a correlation between programming languages and errors, **one that people misinterpreted as a causal relationship.**"
- **Note:** Even the debunking article's headline uses causal language ("lead to more buggy code"). The original 2014 Register coverage (https://www.theregister.com/Print/2014/11/06/languages_dont_breed_bugs_people_breed_bugs) similarly used "breed bugs."
- **Why useful:** Direct testimony from a reproduction study author documenting the misinterpretation phenomenon.

#### Example 2: Edward Huang's Blog (2021) --- "5 Programming Languages That Produce Code Least Prone to Bugs"

- **URL:** https://edward-huang.com/programming/software-development/2021/03/02/5-programming-language-that-produce-code-least-prone-to-bugs/
- **Date:** March 2, 2021
- **Key quotes:**
  - Title: "5 Programming Language That **Produce** Code Least Prone to Bugs"
  - "some programming languages have been designed ... **to help a developer do the right thing**"
  - Cites Ray et al. CACM in the resources section
- **Why useful:** Practitioner blog post that treats associations as intrinsic language properties, using causal verbs ("produce," "eliminate") while citing the study as empirical backing.

#### Example 3: Medium (2024) --- "The Impact of Programming Languages on Bug Frequency"

- **URL:** https://medium.com/@appjungle/the-impact-of-programming-languages-on-bug-frequency-a-detailed-analysis-8b714ea999bb
- **Date:** June 28, 2024
- **Key quotes:**
  - "Python's readability and simplicity are major factors **contributing to** its low bug frequency."
  - "these come at the cost of **increased bug frequency**" (about C++)
  - Title: "The **Impact** of Programming Languages on Bug Frequency"
- **Why useful:** Recent (2024) example showing the misinterpretation continues a decade after the original study. The causal framing ("impact," "contributing to") is embedded in the title.

#### Example 4: Hacker News Discussion (November 2014, thread #8558740)

- **URL:** https://news.ycombinator.com/item?id=8558740
- **Date:** November 4--5, 2014
- **Key quotes:**
  - paulajohnson: "A Haskell project can expect to see 63% of the bug fixes that a C++ project would see. **I don't call a 36% drop in bugs 'small'.**" --- Treats the regression coefficient as a direct causal quantity (switching from C++ to Haskell "would" produce fewer bugs).
  - oskarth: "The data indicates functional languages **are better than** procedural languages"
- **Why useful:** Shows immediate causal interpretation by practitioners within days of publication. Commenters treat regression coefficients as switchable causal effects.

#### Example 5: Slashdot (January 2018) --- "Which Programming Languages Are Most Prone to Bugs?"

- **URL:** https://developers.slashdot.org/story/18/01/01/0242218/which-programming-languages-are-most-prone-to-bugs
- **Date:** January 1, 2018
- **Key observation:** The headline frames bug-proneness as an intrinsic language property ("Which Programming Languages **Are** Most Prone to Bugs?") rather than a confounded association.
- **Why useful:** Major tech news aggregator with causal framing in the headline itself.

#### Usage in Section 4.2

Select 2--3 of the strongest examples (likely #1 for the Berger meta-quote, #4 for practitioner causal interpretation, and #2 or #3 for the blog-post pattern). These are footnotes or brief inline references, not the main evidence --- the quantitative citation analysis (Stream 1) carries the argument.

---

## Writing Order

1. **Run `scripts/fetch_ray_citations.py`:**
   - [ ] Write the script
   - [ ] Run it to produce `data/ray_citations.csv`
   - [ ] Inspect 20--30 citation contexts to finalize classification scheme

2. **Run `scripts/classify_ray_citations.py`:**
   - [ ] Write the script with the finalized classification scheme
   - [ ] Run it to classify all citing papers
   - [ ] Compute summary statistics
   - [ ] Select 3--5 representative quotes for the paper

3. **Write Section 4.2 prose:**
   - [ ] Stream 1 (citation analysis) --- ~2 paragraphs + table/figure
   - [ ] Stream 2 (media examples) --- ~1 paragraph with footnotes
   - [ ] Closing argument and transition --- ~1 paragraph

4. **Update Introduction and Abstract** to reference the literature synthesis and misinterpretation analysis as a contribution.

---

## Length Target

- Section 4.1 (expanded): ~1.5 pages --- DONE
- Section 4.2 (new): ~1.5--2 pages (including one table or figure for citation analysis)
- Total for 4.1 + 4.2: ~3--3.5 pages

---

## Success Criteria

- [x] A reader who knows nothing about the PL-quality debate can understand its full arc after reading 4.1
- [ ] The misinterpretation problem is documented with *quantitative* evidence, not just assertion
- [x] The argument flows naturally from "here is what researchers found" (4.1) -> "here is how it was misinterpreted" (4.2) -> "here is how the pragmatic stance would diagnose and fix it" (4.3--4.4)
- [x] Both Ray et al. and Bogner & Merkel are introduced as part of the literature landscape (4.1) before being used as worked examples (4.3--4.4)
