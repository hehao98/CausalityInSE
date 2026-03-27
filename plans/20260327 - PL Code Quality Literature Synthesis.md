# PL vs. Code Quality Literature Synthesis Plan

**Date:** 2026-03-27
**Scope:** Sections 4.1 (literature synthesis) and 4.2 (misinterpretation problem) of the unified Section 4.
**Goal:** Write a literature synthesis that (a) traces the PL vs. code quality debate as a coherent narrative, (b) documents the downstream misinterpretation problem with quantitative evidence, and (c) argues that the debate's impasse is about *identification*, setting up the two worked examples.

---

## Current State

- **Section 4.1 (three-phase narrative)** is drafted (~20 lines). Covers controlled experiments (Prechelt, Hanenberg, Nanz & Fischbach), observational studies (Ray et al., Meyerovich & Rabkin, Gao et al.), and reproduction/causal identification (Berger et al., Furia et al., Bogner & Merkel).
- **Section 4.2 (misinterpretation)** is a placeholder with a one-line TODO comment.
- The Introduction already previews Ray et al.'s downstream misinterpretation (lines 122--127 of main.tex) and the Hernán (2018) causal language problem (footnote on line 120).

## What Needs to Change

### Section 4.1: Expand the Literature Synthesis

The current draft is compact and effective but needs expansion in three areas:

1. **Broaden the controlled experiments coverage.** Add:
   - Endrikat et al. (2014) --- meta-analysis of type system experiments
   - Fischer et al. (2015) --- effect of type system on API usability
   - Mayer et al. (2012) --- visual/type error experiments (already cited but deserves more context)
   - Key takeaway: experiments consistently show type systems help with *type-related* errors but not *semantic* errors; effect sizes are modest and dwarfed by individual differences.

2. **Expand the observational studies landscape.** Add:
   - Kochhar et al. (2016) --- large-scale study of language features and bug categories
   - Bhattacharya & Neamtiu (2011) --- early large-scale PL-quality study on open-source C/C++ projects
   - Bissyandé et al. (2013) --- popularity, interoperability, and quality of PL ecosystems
   - Key takeaway: multiple independent teams found similar modest associations, which makes the misinterpretation problem *worse* --- replication of an association is not the same as causal identification.

3. **Strengthen the "toward causal identification" thread.** Add:
   - Explicitly note what Furia et al. (2024) found: the causal effect was *different in direction or magnitude* from the associational estimate on the same data --- this is the smoking gun for why associations are not enough.
   - Note the gap: no study uses panel variation or DiD on real-world project data (already stated, but make it the explicit transition to the worked examples).

### Section 4.2: The Misinterpretation Problem (NEW)

This is the major new writing. Structure it as three evidence streams converging on the same conclusion:

#### Stream 1: Quantitative Citation Analysis of Ray et al.

- **Method:** Sample ~50--100 papers citing Ray et al. (2014) or the CACM version (2017) from Semantic Scholar or Google Scholar. Classify each citing paper's interpretation:
  - *Causal*: Cites the study as evidence that language X *causes* more/fewer defects (e.g., "Ray et al. showed that functional languages cause fewer defects").
  - *Correlational/hedged*: Cites the study as showing an association or correlation, with appropriate qualification.
  - *Neutral/tangential*: Cites the study for context (e.g., dataset description, motivation) without interpreting the findings.
- **Expected finding:** A substantial fraction (likely >40%, based on analogous analyses in epidemiology — Haber et al. 2022 found 52%) interpret the findings causally despite the authors' hedged language.
- **Presentation:** Bar chart or table showing the distribution. Quote 3--5 representative examples of causal misinterpretation (with citations).

#### Stream 2: Media and Practitioner Discourse

- Collect 3--5 examples of how Ray et al.'s findings were reported in tech media and practitioner forums. Candidates:
  - Tech blog posts (e.g., "Which programming languages have the fewest bugs?" articles that cite Ray et al.)
  - Hacker News / Reddit discussions
  - Developer conference talks or company engineering blogs
  - The "functional languages are safer" narrative in industry
- Purpose: Show that the misinterpretation is not limited to academic papers; it flows downstream to practitioners who make tooling and language decisions based on this evidence.

#### Stream 3: Classic Misinterpretation Patterns from Other Domains

- Briefly draw parallels to well-documented misinterpretation cases in other fields to show this is a *systemic* pattern, not a one-off:
  - **Epidemiology:** Observational studies on hormone replacement therapy were widely interpreted as causal until RCTs (WHI) showed the opposite effect --- driven by healthy-user bias (identical in structure to the "disciplined-team bias" in PL studies).
  - **Psychology:** The replication crisis showed that many "established" effects were artifacts of flexible analysis and selection bias.
  - **Hernán (2018) argument:** Avoiding causal language does not prevent causal interpretation; it merely obscures assumptions. The solution is not *less* causal language but *more explicit* causal reasoning.
- Keep this brief (1 paragraph with citations) --- the appendix already covers the psychology/epidemiology parallel in detail.

#### Tying It Together

- Conclude Section 4.2 with the argument: The misinterpretation problem is not a failure of individual authors (Ray et al. were appropriately hedged) but a *structural consequence* of the field's lack of causal reasoning infrastructure. When a field asks causal questions but lacks the vocabulary and tools to distinguish association from causation, downstream misinterpretation is inevitable. The pragmatic stance (Section 3.4) provides exactly this infrastructure.
- Transition: "The remainder of this section demonstrates the pragmatic stance's diagnostic and constructive power by applying it to two studies from this debate."

---

## Writing Order

1. **Section 4.2 citation analysis** (do the empirical work first):
   - [ ] Pull citing papers for Ray et al. (2014) and CACM (2017) from Semantic Scholar API
   - [ ] Sample ~50--100 citing papers; retrieve titles and relevant text
   - [ ] Classify interpretations (causal / hedged / neutral) using LLM + manual verification
   - [ ] Compute proportions; select representative quotes
   - [ ] Collect media/practitioner examples (web search)

2. **Write Section 4.2 prose:**
   - [ ] Stream 1 (citation analysis) --- ~2 paragraphs + table/figure
   - [ ] Stream 2 (media examples) --- ~1 paragraph
   - [ ] Stream 3 (cross-domain parallels) --- ~1 paragraph
   - [ ] Closing argument and transition --- ~1 paragraph

3. **Revise Section 4.1:**
   - [ ] Expand controlled experiments paragraph (add Endrikat, Fischer)
   - [ ] Expand observational studies paragraph (add Kochhar, Bhattacharya & Neamtiu, Bissyandé)
   - [ ] Strengthen the "toward causal identification" paragraph (emphasize Furia et al. finding)
   - [ ] Ensure the section reads as a coherent narrative flowing into 4.2

4. **Update Introduction and Abstract** to reference the literature synthesis and misinterpretation analysis as a contribution.

---

## Key References to Verify/Add

### Already cited (verify still in .bib):
- Ray et al. 2014, 2017 (DBLP keys exist)
- Berger et al. 2019 (DBLP key exists)
- Furia et al. 2022, 2024 (DBLP keys exist)
- Bogner & Merkel 2022 (DBLP key exists)
- Prechelt 2000, Hanenberg 2010, Nanz & Fischbach 2015 (DBLP keys exist)
- Gao et al. 2017 (DBLP key exists)
- Meyerovich & Rabkin 2013 (DBLP key exists)
- Hernán 2018, Haber et al. 2022 (non-CS keys)

### Need to add (verify via DBLP / Google Scholar):
- Endrikat et al. 2014 --- "How do API documentation and static type systems affect API usability?"
- Bhattacharya & Neamtiu 2011 --- "Assessing programming language impact on development and maintenance"
- Bissyandé et al. 2013 --- "Popularity, interoperability, and impact of programming languages in 100,000 open source projects"
- Kochhar et al. 2016 --- "Large scale study of multiple programming languages and code quality" (if it exists — verify)
- Any good tech media examples found during the search

### Cross-domain references (already in appendix, may need to cite in main text):
- WHI hormone replacement therapy reversal (Rossouw et al. 2002 or Manson et al. 2003)
- Haber et al. 2022 causal language in observational abstracts

---

## Length Target

- Section 4.1 (expanded): ~1.5 pages (currently ~0.75 pages)
- Section 4.2 (new): ~2 pages (including one table or figure for citation analysis)
- Total for 4.1 + 4.2: ~3.5 pages

---

## Success Criteria

- [ ] A reader who knows nothing about the PL-quality debate can understand its full arc after reading 4.1
- [ ] The misinterpretation problem is documented with *quantitative* evidence, not just assertion
- [ ] The argument flows naturally from "here is what researchers found" (4.1) → "here is how it was misinterpreted" (4.2) → "here is how the pragmatic stance would diagnose and fix it" (4.3--4.4)
- [ ] Both Ray et al. and Bogner & Merkel are introduced as part of the literature landscape (4.1) before being used as worked examples (4.3--4.4)
