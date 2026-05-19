# Improving Accessibility of Sections 3 and 4

**Status:** Complete (2026-05-19)

**Goal:** Make Section 3 (Primer) and Section 4 (Worked Example) accessible to SE researchers familiar with empirical methods but new to the causal inference toolkit, without diluting the technical content.

## Diagnosis

Three patterns make the prose hard to enter for an SE reader without causal-inference training:

1. **The estimand / estimator / estimate / identification quartet is never plainly distinguished.** These four words mean four different things and the rest of the paper hinges on the distinction, but each is introduced mid-paragraph without a deliberate anchor.
2. **Acronym soup builds rapidly.** ATE, ATT, LATE, CATE, DAG, IPW, PSM, OLS, ITS, TWFE, DiD, CITS, RDD, IV, SUTVA, HC1, FE, MSR --- many appear before Section 3 (e.g., abstract says "staggered DiD"; intro names "DAG", "target estimand", "identifying assumptions").
3. **Technical machinery is introduced before its motivation lands.** Conditional ignorability `$(Y(1), Y(0)) \perp D \mid X$` is stated before non-stats readers learn what `\perp` means; the back-door criterion lacks a one-line plain-English version; Oster's $\delta^*$ shows up in Section 4 with a threshold but no prior gloss.

## Strategic Principles

- **Tier the jargon by location.** Pre-Section 3: looser budget, but every new term is glossed on first use. Section 3 (Primer): every new term gets a formal definition *and* a plain-English shadow on the same line. Section 4 and Section 5: re-link via brief reminders rather than re-explaining.
- **Anchor the foundational five-concept loop first.** Estimand, estimator, estimate, identification, identifying assumptions form a closed conceptual unit. Everything else stands on it.
- **Glossary as on-ramp.** Compact table inside Section 3 for fast lookup. (An appendix glossary was considered but dropped as redundant with the in-line table.)
- **Spell out > abbreviate when plausible.** Keep a small core of abbreviations (SE, DAG, ATE/ATT, DiD); spell out the rest in prose. Reserve abbreviations for tables and figures where space matters.

## Action Plan

### A. Foundational Vocabulary (second opening paragraph of Section 3)

- [x] Collapse the foundational vocabulary into a single second paragraph in the Section 3 preamble (no dedicated subsection). Five sentences cover the estimand / estimator / estimate trio, identification, identifying assumptions, and bias, with a pointer to the glossary table.
- [x] No running example in the paragraph itself; the AI coding tools example is introduced once in §3.1 (philosophical) and used throughout the rest of the section.

**Placement decided:** A short paragraph plus glossary table at the start of Section 3 is sufficient; a dedicated subsection read as too long and wordy.

### B. Compact Glossary Table

- [x] Add a glossary table (16 rows) right after the foundational vocabulary paragraph: term, plain-English description, section pointer. Grouped into foundations, estimands, causal structures, and assumptions.

### C. Section 3 (Primer) Sweep

- [x] Reorder the first `(Y(1), Y(0)) \perp D` occurrence so plain English leads the notation in the RCT identifying-assumption sentence (§3.4.1).
- [x] Demote inline jargon: dropped the "(SCM)" abbreviation and the "do-calculus" name from the DAG-limitations footnote.
- [x] Existing prose already provides plain-English shadows after every formal statement in §3.4--§3.5, and acronyms (ATE, ATT, LATE, CATE, SUTVA, RCT, DAG, IV, IPW, RDD, etc.) are already spelled out on first use within each subsection; no further sweep needed.

### D. Section 4 (Worked Example) Revisions

- [x] Added a plain-English preview sentence to the §4.2.3 difference-in-differences subsection opener.
- [x] Reworked the Oster $\delta^*$ paragraph to lead with the intuition over three sentences before invoking the statistic name and threshold.
- [x] Added Table~\ref{tab:longitudinal-estimators} mapping the four DiD-family estimators (TWFE, CITS, Callaway \& Sant'Anna, Borusyak) to one-line descriptions, ordered from least to most credible.
- [x] Other subsection openers (§4.1.1 naïve comparison, §4.1.4 DAG-justified regression, §4.1.5 sensitivity analysis, §4.1.6 estimator comparison, §4.2.1 before/after, §4.2.2 ITS) already led with plain English; no further changes needed. Full names for PSM / IPW were already in place on first use.

### E. Section 5 (Discussion) Light Touch

- [x] Added a brief inline gloss on conditional ignorability ("---that all confounders are measured and adjusted for---").
- [x] Glossed the ATT inline ("the average effect among the adopting projects").
- [x] Glossed SUTVA violations inline ("one project's treatment status affects another project's outcomes, breaking the no-interference assumption").
- [x] Glossed conditional average treatment effects inline (estimate how the treatment effect varies with covariates).

### F. Pre-Section 3 (Abstract, Introduction, Background)

- [x] **Abstract:** glossed "identifying assumptions" inline ("the conditions under which its analysis admits a causal interpretation") and replaced "DAG-guided cross-sectional analysis" with "cross-sectional analysis guided by a directed acyclic graph (DAG)"; replaced "staggered DiD" with "a difference-in-differences design that handles staggered adoption."
- [x] **Introduction (Section 1):** added em-dash glosses for confounders, mediators, colliders, parallel trends, and continuity at the threshold; tied the latter two to their respective designs (DiD, RDD). Also fixed two "invert probability weighting" $\to$ "inverse probability weighting" typos.
- [x] **Background (Section 2.1):** added a one-sentence opener pointing readers to Section~\ref{sec:primer} for formal definitions of the technical vocabulary.

## Execution Summary

1. Foundational vocabulary paragraph (A) --- the conceptual scaffold. *(Done.)*
2. Compact glossary table (B) --- piggybacks on (A). *(Done.)*
3. Pre-Section 3 sweep (F). *(Done.)*
4. Section 3 sweep (C). *(Done.)*
5. Section 4 revisions (D). *(Done.)*
6. Section 5 touch-up (E). *(Done.)*
