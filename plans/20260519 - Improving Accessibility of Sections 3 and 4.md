# Improving Accessibility of Sections 3 and 4

**Status:** Draft (2026-05-19)

**Goal:** Make Section 3 (Primer) and Section 4 (Worked Example) accessible to SE researchers familiar with empirical methods but new to the causal inference toolkit, without diluting the technical content.

## Diagnosis

Three patterns make the prose hard to enter for an SE reader without causal-inference training:

1. **The estimand / estimator / estimate / identification quartet is never plainly distinguished.** These four words mean four different things and the rest of the paper hinges on the distinction, but each is introduced mid-paragraph without a deliberate anchor.
2. **Acronym soup builds rapidly.** ATE, ATT, LATE, CATE, DAG, IPW, PSM, OLS, ITS, TWFE, DiD, CITS, RDD, IV, SUTVA, HC1, FE, MSR --- many appear before Section 3 (e.g., abstract says "staggered DiD"; intro names "DAG", "target estimand", "identifying assumptions").
3. **Technical machinery is introduced before its motivation lands.** Conditional ignorability `$(Y(1), Y(0)) \perp D \mid X$` is stated before non-stats readers learn what `\perp` means; the back-door criterion lacks a one-line plain-English version; Oster's $\delta^*$ shows up in Section 4 with a threshold but no prior gloss.

## Strategic Principles

- **Tier the jargon by location.** Pre-Section 3: looser budget, but every new term is glossed on first use. Section 3 (Primer): every new term gets a formal definition *and* a plain-English shadow on the same line. Section 4 and Section 5: re-link via brief reminders rather than re-explaining.
- **Anchor the foundational five-concept loop first.** Estimand, estimator, estimate, identification, identifying assumptions form a closed conceptual unit. Everything else stands on it.
- **Glossary as on-ramp + canonical reference.** Compact table at the start of Section 3 for fast lookup; fuller version in an appendix that can be removed later if it proves unnecessary.
- **Spell out > abbreviate when plausible.** Keep a small core of abbreviations (SE, DAG, ATE/ATT, DiD); spell out the rest in prose. Reserve abbreviations for tables and figures where space matters.

## Action Plan

### A. Foundational Vocabulary Subsection (new section in Section 3)

- [ ] Draft a new subsection at the start of Section 3 anchoring the five-concept loop:
  1. **Estimand** --- the target quantity (*what you want to know*).
  2. **Estimator** --- the recipe (*a procedure that maps your dataset to a number*).
  3. **Estimate** --- the number (*the output of running the estimator on your specific sample*).
  4. **Identification** --- the conditions under which the estimator's expected output equals the estimand.
  5. **Identifying assumptions** --- the specific, defensible claims that secure identification in a given study (random assignment, conditional ignorability, parallel trends, etc.).
- [ ] Briefly mention --- but do not formalize:
  - **Bias** as "what fills the gap when the identifying assumptions fail" (ties to selection/collider/mediator bias discussed later).
  - **Treatment, outcome, unit, population** as a reminder that defining the contrast carefully is itself a causal-inference task (forward pointer to the target-trial discussion).
- [ ] Use one running SE example throughout the subsection (e.g., "the average effect of adopting code review on defect rate") so the five abstract concepts get concrete anchors.

**Open question:** Placement vs. the existing §3.1 "What Does It Mean Exactly for X to Cause Y?"
- *Option (a) --- Vocabulary first:* new subsection becomes §3.1, push the philosophical view (counterfactual dependence + three necessary conditions) to §3.2. Recommended.
- *Option (b) --- Philosophy first:* keep current §3.1, insert vocabulary as §3.2 before potential outcomes.

### B. Compact Glossary Table at Start of Section 3

- [ ] Add a glossary table (~12--15 rows) right after the foundational subsection: term, plain-English description, formal reference (section pointer). Each row $\leq$ 80 characters.
- [ ] Initial candidate entries: confounder, collider, mediator, back-door path, counterfactual, potential outcome, ATE, ATT, parallel trends, DAG, target trial, conditional ignorability, SUTVA.

### C. Section 3 (Primer) Sweep

- [ ] Add a one-sentence plain-English shadow after every formal statement (some subsections already do this; others do not).
- [ ] Replace `\perp`-style notation with words on first use: "treatment is independent of potential outcomes given $X$, written $(Y(1), Y(0)) \perp D \mid X$."
- [ ] Demote some inline jargon (do-calculus, Berkson's paradox, $d$-separation) into "see the references" rather than naming the concept in the main text.
- [ ] Spell out abbreviations on first use within each subsection.

### D. Section 4 (Worked Example) Revisions

- [ ] Open each subsection with a one-sentence "what this method does in plain English, what assumption it buys" preview before any formula.
- [ ] Reduce acronym density: on first use per subsection, use full names ("propensity score matching", "inverse probability weighting") before abbreviating.
- [ ] Rework the Oster $\delta^*$ paragraph (§3.5 / §sec:cross-sectional-sensitivity) to lead with plain English before invoking the threshold.
- [ ] Add a small "method name $\to$ one-sentence description" subtable for the CS / Borusyak / TWFE / CITS quartet in the longitudinal subsection.

### E. Section 5 (Discussion) Light Touch

- [ ] Add brief inline reminders (one clause each) for "conditional ignorability", "ATT", "SUTVA violations", "double/debiased machine learning"; or point back to the Section 3 glossary entry.

### F. Pre-Section 3 (Abstract, Introduction, Background)

- [ ] **Abstract:** keep "identifying assumptions" (a thesis word) but add a one-clause gloss; replace "staggered DiD" with "a difference-in-differences design that handles staggered adoption."
- [ ] **Introduction (Section 1):** each named term ("target estimand", "identifying assumptions", "natural experiment", "parallel trends", "continuity at the threshold", "mediators", "colliders") gets a parenthetical or em-dash gloss on first appearance; deep definitions deferred to Section 3.
- [ ] **Background (Section 2.1):** open with an explicit statement that the technical vocabulary used in this subsection is defined in Section 3.

### G. Appendix Glossary

- [ ] Add a new appendix subsection with the fuller glossary: every technical term, 2--3 sentences each, with section pointers. This is the canonical reference; the table in Section 3 is the on-ramp. Removable later if it proves redundant.

## Execution Order (suggested)

1. Foundational vocabulary subsection (A) --- the conceptual scaffold.
2. Compact glossary table (B) --- piggybacks on (A).
3. Pre-Section 3 sweep (F) --- low-effort, eliminates the worst friction for first-time readers.
4. Section 3 sweep (C) --- depends on (A) for anchors.
5. Section 4 revisions (D).
6. Appendix glossary (G).
7. Section 5 touch-up (E).
