# Plan: Merging Section 4 into Section 3.4

**Date:** 2026-03-27

**Goal:** Remove Section 4 ("A Guide for Conducting Credible Causal Inquiries in SE") by absorbing its genuinely new content into Section 3.4 ("A Pragmatic Stance for SE Research"), which already has the desired style. Add a new point on the role of prior SE research and gray literature in theory generation and DAG construction.

---

## Problem

Section 4 was written as a "practical guide" that operationalizes Section 3.4's pragmatic stance. In practice, the overlap is extensive:

| Section 4 Content | Already Covered In |
|---|---|
| Target trial (4.1 ¶1) | Section 3.4 ¶1 ("Use Counterfactual Reasoning") |
| Define estimand (4.1 ¶2) | Section 3.2 (Potential Outcomes), Section 3.4 ¶1 |
| Construct preliminary DAG (4.1 ¶3) | Section 3.4 ¶2 ("Use DAGs"), Section 3.3 (DAGs) |
| Path A procedure (4.2.1) | Section 3.3 (back-door criterion, covariate selection) |
| Path A sensitivity analysis (4.2.1) | Section 3.2 footnotes (Rosenbaum bounds, E-value, etc.) |
| Path B: design-based methods (4.2.2) | Section 3.4 ¶3 ("Use Design-Based Identification"), Section 3.5 |
| Parallel trends / F-tests / McCrary (4.2.2) | Section 3.5 (each method's assumptions) |
| Sensitivity analysis tools list (4.3) | Section 3.2 footnotes |

Section 3.4 already says the same things in a more concise, opinionated, well-paced style. Section 4 mostly re-explains at greater length what the primer + 3.4 already teach.

---

## Genuinely New Content in Section 4 Worth Preserving

These points are NOT adequately covered in Section 3 and should migrate into Section 3.4:

1. **Iteration between target trial, estimand, and DAG** (4.1 ¶4, lines 667-671): The three activities are iterative, not sequential. Constructing the DAG may reveal the treatment is poorly defined; defining the estimand may reveal which identification strategies are feasible. Short but important meta-point.

2. **Table: Data features → design-based methods** (4.2.2, Table 2, lines 719-737): Compact, actionable mapping (panel data → panel FE, staggered adoption → DiD, external shock → IV, threshold → RDD) with SE examples. This table is genuinely useful as a quick-reference companion to ¶3.

3. **"When Neither Path Is Clean" — Reformulation** (4.2.3, lines 753-771): The idea that a researcher can *reformulate* the causal question to exploit available variation (e.g., "Does language affect quality?" → "Does adopting a type system reduce defects?"). This is the most creative and valuable act in a causal inquiry. Triangulation across imperfect approaches. Honest framing: transparent uncertainty is a contribution; false certainty is a liability.

4. **Three patterns of alternative explanations** (4.3, lines 799-811): Alternative mechanism, unmeasured confounding, reverse causality — each with a diagnostic test. Concise and actionable.

5. **SE-specific measurement challenges** (4.3, line 794): Noisy proxies for latent constructs, construct validity issues, SUTVA violations in interconnected ecosystems. Brief but field-specific.

6. **"Limitations should be mitigated, not merely listed"** (4.3, lines 779-781): Direct critique of the SE tradition of boilerplate "threats to validity" sections.

---

## New Content to Add: Prior SE Research and Gray Literature for Theory Generation

**Motivation:** Section 3.4 ¶2 says "Use DAGs to Reason About Mechanisms" but doesn't say where the domain knowledge for DAG construction comes from. Section 3.3 (DAGs, "Limitations of DAGs") notes that DAGs require domain knowledge, but doesn't acknowledge the sources. We need to explicitly recognize:

- **Prior empirical SE research** — even correlational or descriptive studies — provides the raw material for proposing causal structures. A correlational finding that "projects using static analysis have fewer bugs" is not itself causal evidence, but it motivates an edge in the DAG that can then be subjected to rigorous identification.
- **Gray literature** (blog posts, postmortems, industry reports, developer surveys, practitioner talks) encodes practitioner causal beliefs ("we adopted X and it reduced Y") that are valuable for theory generation, even if anecdotal.
- **Qualitative SE research** (interviews, case studies, grounded theory) provides rich mechanistic accounts that inform DAG structure.
- This creates a virtuous cycle: Prior descriptive/correlational work generates theories (DAGs), which are then tested with rigorous causal methods, whose findings refine the theories.
- This framing is important because it does NOT dismiss the existing body of SE research — it reframes it as an essential foundation for the more rigorous causal work the paper advocates.

---

## Proposed Structure for Expanded Section 3.4

Keep the existing `\paragraph{}` style. The expanded section should have ~8-9 paragraphs (up from 5), staying concise and opinionated. Estimated length: ~1.5 pages (up from ~1 page).

The expanded section uses the same `\paragraph{}` style as the current 3.4. The ordering follows a natural arc: *know the territory* → *what to do* → *how the process works* → *when it gets hard* → *why it fits your field*.

### ¶1 NEW "Build on Prior Research and Practitioner Knowledge."

Comes first because the researcher needs to ground themselves in existing knowledge before they can frame a question, sketch a DAG, or choose a method. This paragraph:
- Acknowledges that prior empirical SE research — even correlational or descriptive — provides the raw material for proposing causal structures and arguing that causal testing is important. A finding that "projects using static analysis have fewer bugs" motivates a DAG edge that can then be subjected to rigorous identification.
- Gray literature (blog posts, postmortems, industry reports, practitioner talks) and qualitative SE research (interviews, case studies) encode practitioner causal beliefs that are valuable for theory generation.
- Frames a virtuous cycle: prior descriptive/correlational work generates theories (DAGs) → causal methods test them → findings refine theories.
- This is important because it does NOT dismiss the existing body of SE research — it reframes it as an essential foundation for the more rigorous causal work the paper advocates.

### ¶2 KEEP "Use Counterfactual Reasoning to Frame Research Designs."

Keep as is. Add a sentence about the four dimensions (treatment, population, outcome, timing) that the target trial forces clarity on.

### ¶3 KEEP "Use DAGs to Reason About Mechanisms and Covariate Selection."

Keep as is. Now reads naturally after ¶1 (prior research provides the domain knowledge) and ¶2 (target trial frames the question).

### ¶4 KEEP "Use Design-Based Identification When the Setting Permits."

Keep as is. Attach Table 2 (data features → methods) as a companion.

### ¶5 NEW "Iterate Between Question, Assumptions, and Design."

From Section 4.1 ¶4. The three activities (target trial, estimand, DAG) are iterative; insights at any stage may send the researcher back. This is not a failure of planning but integral to rigorous causal reasoning. Placed after the three recommendations (¶2–4) as a meta-point connecting them.

### ¶6 NEW "When Clean Identification Is Unavailable."

From Section 4.2.3. Many SE settings offer neither full covariate coverage nor quasi-experimental variation. Pragmatic response: use the best available strategy with honest sensitivity analysis; consider reformulating the question to exploit available variation; triangulate across imperfect approaches. Transparent uncertainty is a contribution.

### ¶7 NEW "Engage with Alternative Explanations."

From Section 4.3. Three patterns (alternative mechanism, unmeasured confounding, reverse causality) with diagnostic tests. Limitations should be mitigated, not merely listed. SE-specific measurement challenges (noisy proxies, SUTVA violations).

### ¶8 KEEP "Why This Stance Fits SE."

Keep as is, as the closing argument. Remove the forward pointer to Section 4 (which will no longer exist). Keep or update the pointer to the appendix empirical standard.

---

## Downstream Changes

### Remove Section 4

Delete lines 621–811 entirely. This removes:
- The intro paragraphs (lines 621–633)
- 4.1 "Start with the Causal Question" (lines 635–671)
- 4.2 "Two Paths to Identification" (lines 673–771)
- 4.3 "Probing Credibility" (lines 773–811)

### Renumber subsequent sections

| Current | New |
|---|---|
| Section 4: Guide | *removed* |
| Section 5: Worked Example A | Section 4: Worked Example A |
| Section 6: Worked Example B | Section 5: Worked Example B |
| Section 7: Discussion | Section 6: Discussion |
| Section 8: Conclusion | Section 7: Conclusion |

### Update cross-references

- All `\ref{sec:guide*}` references throughout the paper need updating.
- The worked examples (current Sections 5-6) reference the guide's subsections (e.g., "As the guide in Section 4 recommends..."). These should be rewritten to reference Section 3.4 instead.
- Introduction and abstract references to "the guide" or "Section 4" need updating.
- Section 3.4's forward pointer to Section 4 should be removed or rewritten to point to the appendix standard.
- Check that Table 2 (data features → methods) doesn't conflict with being moved into Section 3.4 alongside the existing Table 1 (methods summary) in Section 3.5.

### Preserve Table 2 (data features → methods)

Move Table 2 from Section 4.2.2 into Section 3.4, near the "Use Design-Based Identification" paragraph. Ensure it doesn't duplicate information in Table 1 (methods summary in Section 3.5) — the two tables serve different purposes (Table 1: estimands and assumptions; Table 2: data features as entry points).

### Worked examples references

The worked examples currently reference the guide structure ("As the guide recommends, we begin by articulating the target trial..."). These callbacks should be updated to reference Section 3.4's pragmatic stance instead. The references should still work because the key concepts (target trial, DAG, identification paths) all remain in 3.4.

---

## Actionable Tasks

- [ ] Read the full intro and abstract to inventory all references to "Section 4" / "the guide"
- [ ] Draft expanded Section 3.4 with 8-9 paragraphs following the structure above
- [ ] Remove Section 4 (lines 621–811)
- [ ] Move Table 2 (data features → methods) into Section 3.4
- [ ] Update all `\ref{sec:guide*}` cross-references
- [ ] Update worked examples (Sections 5-6 → 4-5) to reference Section 3.4
- [ ] Update introduction and abstract references
- [ ] Verify the appendix standard's cross-references still work
- [ ] Read through the merged section for flow, redundancy, and tone consistency
