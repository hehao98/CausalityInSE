# Revising Section 3.1: Views of Causality

**Created:** 2026-05-19
**Last updated:** 2026-05-19 (target trial relocates to Section 3.4 instead
of Section 3.3.3 — merged into existing workflow paragraph rather than
promoted as a new section opener)
**Status:** Approved — ready to begin drafting paragraphs

## Motivation

Section 3.1 ([paper/2-primer.tex:9-37](../paper/2-primer.tex#L9-L37)) currently
presents two "views of causality" to motivate the primer toolkit:

1. **Causation as Counterfactual Dependence** (Rubin/Lewis) at
   [2-primer.tex:20-26](../paper/2-primer.tex#L20-L26).
2. **Causation as a Target Trial** (Hernán) at
   [2-primer.tex:28-34](../paper/2-primer.tex#L28-L34).

Two issues with the current framing motivate revision:

### Issue 1: The target trial paragraph is structurally mis-filed

The section heading asks "What Does It Mean Exactly for X to Cause Y?" — a
question about the *definition* of causation. The closing paragraph at
[2-primer.tex:36-37](../paper/2-primer.tex#L36-L37) concedes that target trial
is in fact a *research-design template*, not a definition:

> "the counterfactual view defines the target … while the target trial view
> provides the research design template."

This conflates two distinct things — what causation means versus how a
researcher operationalizes a study around it. Target trial is genuinely
load-bearing later in the paper (it is the conceptual hook for the natural-
experiment framing in Section 3.3.3 at
[2-primer.tex:232](../paper/2-primer.tex#L232) and the "Use Counterfactual
Reasoning to Frame Research Designs" paragraph in Section 3.4 at
[2-primer.tex:329-334](../paper/2-primer.tex#L329-L334)), so it should stay in
the paper, but not as a definition of causality.

### Issue 2: A widely-used SE framing is missing

A classical three-conditions view of causality, often credited to Rosenbaum
(2002) but with deeper roots in Bradford Hill (1965) and earlier social-science
methods literature, is the methodological backbone of an active SE research
line — particularly cohort-style observational studies in MSR/ESEM/EMSE. The
three conditions are:

1. **Temporal precedence.** The cause must precede the effect.
2. **Empirical association.** A statistical relationship between cause and
   effect must be observable.
3. **Non-spuriousness.** The relationship must not be due to confounders.

SE invocations of this framework span at least three genuinely distinct
clusters (lit sweep, 2026-05-19):

### Cluster 1 — CMU empirical-methods pedagogy (Vasilescu)

- **Bogdan Vasilescu**, CMU 17-803 *Empirical Methods*, Lecture 13:
  *Designing Experiments I — Causal Relationships* (Spring 2026).
  - Slides: <https://bvasiles.github.io/empirical-methods/slides/13-experiments-pt1.pdf>
  - Slide 10 ("Ingredients for Establishing a Causal Relationship"):
    *"The cause preceded the effect / The cause was related to the effect /
    We can find no plausible alternative explanation for the effect other
    than the cause."*
  - Cited basis: Shadish, Cook & Campbell (2002), *Experimental and
    Quasi-Experimental Designs for Generalized Causal Inference.*
  - **Distinct because:** CMU STRUDEL lab (OSS sustainability, gender in
    OSS, GitHub badges); framing is experimental / quasi-experimental
    pedagogy, not propensity-matched cohorts; teaches the framework to a
    full PhD-cohort audience each year.

### Cluster 2 — UT Austin empirical-SE foundations (Perry)

- **Dewayne E. Perry**, UT Austin 382C *Empirical Studies in Software
  Engineering*, Lecture 5: *Underlying Theory and Basic Issues.*
  - Slides: <https://users.ece.utexas.edu/~perry/education/382c/L05.pdf>
  - Slide 21 ("Distillation"): *"Co-variation Rule: cause is positively
    correlated with effect / Temporal Precedence Rule: causes must precede
    effects / Internal Validity Rule: all plausible alternative
    explanations must be ruled out."*
  - Cited basis: Campbell, Stanley & Cook; Hume; Mill's methods.
  - **Distinct because:** Foundational figure in SE
    experimentation-validity discourse (cited by Wohlin et al.'s
    experimentation textbook); decade-different lineage from Saarimäki.

### Cluster 3 — Tampere/Oulu/UPM cohort studies (Saarimäki et al.)

This is the original cluster, still worth a one-line acknowledgment but no
longer the primary evidence base:

- Saarimäki et al. *EMSE 30(5)* 2025; Saarimäki et al. *ESEM 2020*;
  Nocera et al. *FSE Companion 2025*; the ICSE 2026 "Causal or
  Correlational?" code-smells cohort paper that prompted this revision.

Across three clusters — pedagogy at CMU, pedagogy at UT Austin, and cohort
studies at Tampere/Oulu/UPM — the three-conditions framing is clearly more
than one author's idiosyncrasy. **Two of the three clusters are
graduate-level teaching materials**, which means a non-trivial share of SE
PhD students are taught this framework as the primary definition of
causation. Omitting it from our primer would be conspicuous to those
readers. Both `hill1965environment` and `rosenbaum2002observational` are
already in the bibliography but neither is cited from Section 3.1 today;
the pedagogy clusters suggest that the canonical SE citation may actually
be **Shadish, Cook & Campbell (2002)** rather than Rosenbaum, since both
pedagogy lineages cite SCC (or the Cook & Campbell 1979 predecessor) and
the Wohlin et al. experimentation textbook derives from the same lineage.

## Plan: Two views in Section 3.1; relocate target trial and intervention

The pedagogical question driving this plan: *How many distinct "views of
causation" can an SE reader with no prior causal-inference background absorb
before they reach the toolkit?* The current paper presents two (counterfactual
+ target trial) in the body and two more (Hume regularity + Pearl
intervention) in the footnote. That is too many for a primer, and two of those
four are not actually *definitions* of causation:

- **Target trial** is a *workflow exercise* (a brainstorming step for the
  researcher), not a method on equal footing with DiD/IV/RDD. It belongs
  in Section 3.4's design-stance paragraph at
  [2-primer.tex:329-334](../paper/2-primer.tex#L329-L334), which already
  invokes target trial in exactly that spirit. Placing it at the opening
  of Section 3.3.3 would implicitly elevate it to peer status with the
  methods table and concentrate jargon in an already-dense section.
- **Pearl's interventionist view** is *what DAGs encode.* Promoting it to its
  own definition paragraph in Section 3.1 forces the reader to absorb
  do-calculus notation before the toolkit has been introduced. Worse, the
  current Section 3.1 already uses `do(X)` at
  [2-primer.tex:34](../paper/2-primer.tex#L34) without ever defining it. The
  natural home for the interventionist view is Section 3.3.2, introduced
  alongside DAGs themselves.

Section 3.1 should therefore present exactly two views:

- [ ] **Causation as Counterfactual Dependence** (Rubin/Lewis) — the
  abstract definition. Keep substantively as-is from
  [2-primer.tex:20-26](../paper/2-primer.tex#L20-L26). This view is
  irreducible because the potential outcomes framework (Section 3.3.1)
  formalizes exactly this definition.
- [ ] **Causation as Three Necessary Conditions** (Hill 1965; Cook &
  Campbell 1979; Rosenbaum 2002; Shadish, Cook & Campbell 2002) — new
  paragraph. The operational definition. Map each condition to the toolkit
  pillar that addresses it:
  - Temporal precedence → panel data, DiD, longitudinal designs
    (Section 3.3.3 + Section 4).
  - Empirical association → estimation under correct specification.
  - Non-spuriousness → DAGs and the back-door criterion (Section 3.3.2);
    IV and design-based identification (Section 3.3.3).
  - Cite 2-3 SE-community examples across distinct clusters: Vasilescu's
    CMU 17-803 lecture, Perry's UT Austin 382C lecture, and one
    representative paper from the Saarimäki/Lenarduzzi cohort line
    (e.g., ESEM 2020 vision paper or the ICSE 2026 code-smells paper).
  - Add a one-sentence framing that this view is **complementary, not
    competing** with the counterfactual view: the three conditions are
    necessary but not sufficient, and they can be derived as consequences
    of counterfactual reasoning. This defends against a Pearl/Rubin-purist
    reviewer.

Relocations (deletions from Section 3.1, additions elsewhere):

- [ ] **Merge target trial into Section 3.4 rather than relocating it as
  a standalone paragraph.** Section 3.4 already has a "Use Counterfactual
  Reasoning to Frame Research Designs" paragraph at
  [2-primer.tex:329-334](../paper/2-primer.tex#L329-L334) that invokes
  target trial as a brainstorming exercise. Take ~2 sentences of
  conceptual setup from the current Section 3.1 paragraph — the *"every
  causal question implicitly describes a hypothetical randomized
  experiment"* hook and the velocity-example clauses showing how
  articulating the trial reveals threats to validity (selection,
  ambiguous treatment, proxy outcomes) — and fold them into the existing
  Section 3.4 paragraph. No new heading, no new jargon, just a slightly
  richer existing paragraph.
- [ ] **Soften the forward reference at
  [2-primer.tex:232](../paper/2-primer.tex#L232).** The current Section
  3.3.3 opening says *"approximate the ideal target trial"* — which
  becomes a forward reference once target trial is introduced for the
  first time in Section 3.4. Either drop the phrase ("approximate an
  ideal experiment") or keep it as a casual aside with no formal load.
  The Hernán citation can stay either way.
- [ ] **Delete the closing two-sentence "complementary perspectives"
  paragraph** at [2-primer.tex:36-37](../paper/2-primer.tex#L36-L37).
  Replace with a single sentence at the end of Section 3.1 that previews
  the toolkit: the two views together motivate the three-pillar toolkit
  introduced in Section 3.3.
- [ ] **Move Pearl's interventionist view to Section 3.3.2.** Delete the
  Pearl-and-do-calculus content from the current footnote at
  [2-primer.tex:15-18](../paper/2-primer.tex#L15-L18) (keep only the brief
  Hume reference, since it sets up *why* the counterfactual view was
  needed). Add a sentence to the opening of Section 3.3.2 framing DAGs as
  the formalization of Pearl's interventionist view of causation. The
  `do(X)` notation should be introduced there, not in Section 3.1.
- [ ] **Strip the `do(X)` notation from Section 3.1.** The current text at
  [2-primer.tex:34](../paper/2-primer.tex#L34) uses `P(Y|X=1)` vs.
  `P(Y|do(X=1))` to contrast seeing vs. doing. Rephrase in plain English
  ("observing that AI-adopting projects have more commits" vs. "intervening
  to make a project adopt AI tools"), and defer the formal notation to
  Section 3.3.2.

Downstream consistency checks:

- [ ] No cross-reference update needed in Section 3.4 — target trial is
  introduced for the first time *in* Section 3.4 itself, in the existing
  paragraph at
  [2-primer.tex:329-334](../paper/2-primer.tex#L329-L334). The
  current internal reference at
  [2-primer.tex:331](../paper/2-primer.tex#L331) (`\label{sec:guide-question}`)
  stays valid.
- [ ] Verify Section 3.2 ("Why Cannot We Use Descriptive and Correlational
  Evidence?") still flows. The three-conditions view actually *strengthens*
  the lead-in: Section 3.2 is essentially a demonstration that naive
  comparisons fail non-spuriousness, and the temporal precedence condition
  motivates the reverse-causality subsection at
  [2-primer.tex:71-73](../paper/2-primer.tex#L71-L73).
- [ ] Verify Section 3.3.1 still flows. Its opening sentence at
  [2-primer.tex:98](../paper/2-primer.tex#L98) says PO "formalizes the
  counterfactual view of causation introduced in Section 3.1" — this
  reference stays valid since counterfactual is still in Section 3.1.

## Rationale

This plan (a) honors a real SE sub-community that uses the three-conditions
framing, (b) repairs an internal inconsistency that the section already
concedes, (c) **reduces the jargon load on a newcomer SE reader** by keeping
Section 3.1 down to two clean view-names (one abstract, one operational)
instead of three or four, (d) puts the interventionist view and `do(X)`
notation where they actually belong (with DAGs in Section 3.3.2), and (e)
costs roughly two paragraph rewrites plus relocating two paragraphs. No
figure or downstream section needs structural change, and the
cross-references are bounded.

## Tasks

### Section 3.1 rewrites

- [ ] Draft new **"Causation as Three Necessary Conditions"** paragraph
  (target: ~6-8 sentences, following the setup-formalism-interpretation
  rhythm from `paper/AGENTS.md`). The paragraph should:
  - State the three conditions concisely.
  - Map each condition to the toolkit pillar that addresses it.
  - Cite 2-3 SE examples spanning distinct clusters.
  - Close with a complementarity sentence (three conditions are necessary
    but not sufficient; derivable from counterfactual reasoning).
- [ ] Keep the **"Causation as Counterfactual Dependence"** paragraph
  substantively as-is; only minor edits to flow into the new
  three-conditions paragraph instead of into target trial.
- [ ] Trim the existing Section 3.1 footnote at
  [2-primer.tex:15-18](../paper/2-primer.tex#L15-L18) to retain only the
  Hume-regularity sentence (or drop the footnote entirely). Move the
  Pearl/intervention content to Section 3.3.2 (see below).
- [ ] Rewrite the seeing-vs.-doing sentence currently at
  [2-primer.tex:34](../paper/2-primer.tex#L34) in plain English; defer
  `do(X)` notation to Section 3.3.2.
- [ ] Replace the closing two-sentence paragraph at
  [2-primer.tex:36-37](../paper/2-primer.tex#L36-L37) with a single
  one-sentence preview of the three-pillar toolkit.

### Relocations

- [ ] **Merge target trial into Section 3.4's existing workflow
  paragraph** at
  [2-primer.tex:329-334](../paper/2-primer.tex#L329-L334). Take the
  *"every causal question implicitly describes a hypothetical randomized
  experiment"* hook and the velocity-example clauses about threats to
  validity from the current Section 3.1 paragraph, and weave them into
  the existing paragraph. Aim for ~2-3 extra sentences, not a full
  paragraph replacement. The existing paragraph's framing ("Before
  analyzing data, articulate the target trial") stays as the topic
  sentence.
- [ ] **Soften the forward reference** at
  [2-primer.tex:232](../paper/2-primer.tex#L232) in Section 3.3.3 —
  either drop "target trial" (use "ideal experiment") or keep as casual
  aside. The Hernán citation can stay either way.
- [ ] Move the **Pearl/intervention** content from the Section 3.1 footnote
  to the opening of Section 3.3.2 at
  [2-primer.tex:129-134](../paper/2-primer.tex#L129-L134). Introduce
  `do(X)` notation here, where DAGs are about to be formalized as the
  graphical encoding of interventions.

### Cross-references and downstream consistency

- [ ] Confirm Section 3.3.1 opening at
  [2-primer.tex:98](../paper/2-primer.tex#L98) ("formalizes the
  counterfactual view of causation introduced in Section 3.1") still reads
  correctly.
- [ ] Confirm Section 3.2 transition still flows; the three-conditions
  view actually strengthens it (non-spuriousness motivates the whole
  section; temporal precedence motivates the reverse-causality subsection
  at [2-primer.tex:71-73](../paper/2-primer.tex#L71-L73)).
- [ ] Confirm Section 3.4's `\label{sec:guide-question}` and
  `\label{sec:stance-prior-research}` anchors at
  [2-primer.tex:321,330](../paper/2-primer.tex#L321) remain valid —
  no callers elsewhere in the paper need updating.

### Bibliography

- [ ] `rosenbaum2002observational` (already in bib) — cite from new
  paragraph.
- [ ] `hill1965environment` (already in bib) — cite from new paragraph.
- [ ] Add **Shadish, Cook & Campbell (2002)**, *Experimental and
  Quasi-Experimental Designs for Generalized Causal Inference* to
  `paper/refs.bib`. This is the canonical SE citation for the
  three-conditions view (cited by Vasilescu's slides and the Perry
  lineage); should be the *primary* citation alongside Rosenbaum.
- [ ] Pick 2-3 SE-community examples to cite. Candidates:
  - [ ] **Vasilescu CMU 17-803 lecture slides** — `@online` entry with
    the slide URL and a `note={Accessed YYYY-MM-DD}` field per
    `paper/AGENTS.md` conventions for online resources.
  - [ ] **Perry UT Austin 382C lecture slides** — same format.
  - [ ] Saarimäki et al. ESEM 2020 (cohort studies vision) — DBLP entry.
  - [ ] ICSE 2026 code-smells cohort paper — DBLP entry (verify
    indexing).
- [ ] **Recommended citation mix in the new paragraph:** the two
  pedagogy clusters (Vasilescu + Perry) plus one paper from the cohort
  cluster (Saarimäki ESEM 2020 or the ICSE 2026 paper). This signals
  that the framework is taught *and* practiced in SE across
  independent communities.

### Validation

- [ ] Build the PDF and visually check Section 3.1 fits within the existing
  page budget (the net change should be roughly neutral: +1 paragraph in
  3.1, –2 paragraphs because target trial and interventionist move out).
- [ ] Re-read Section 3.2 end-to-end and confirm the new three-conditions
  framing improves the lead-in (non-spuriousness motivates the whole
  section; temporal precedence motivates the reverse-causality subsection).
- [ ] Re-read the rewritten Section 3.3.2 opening and confirm `do(X)`
  notation is introduced cleanly before first use.
- [ ] Re-read the rewritten Section 3.3.3 opening and confirm that
  softening the "target trial" forward reference reads cleanly.
- [ ] Re-read the merged Section 3.4 workflow paragraph and confirm
  target trial reads as a brainstorming exercise (not a method) and that
  the velocity example threads through naturally without doubling back
  to material already covered in Section 3.2.

## Out of Scope

- Rewriting Section 3.3 (the toolkit pillars themselves).
- Changing the worked-example sections (Section 4 onward).
- Adding a deeper philosophical discussion of additional accounts (e.g.,
  process theories, mechanistic accounts) — the existing footnote at
  [2-primer.tex:15-18](../paper/2-primer.tex#L15-L18) already gestures at
  these and we should not expand further given page constraints.
