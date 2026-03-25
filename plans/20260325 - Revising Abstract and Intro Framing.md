# Plan: Revising the Abstract, Introduction, and Section 2 Framing

**Goal:** Shift the paper's opening narrative from "SE is in crisis like psychology" to a more measured framing: "SE has productively relied on descriptive, correlational, and qualitative evidence, but for a specific class of problems---those about interventions and their outcomes---this evidence is unsatisfying, and in extreme cases produces controversy."

---

## Problem Diagnosis

The current abstract and introduction frame the paper around a **crisis analogy**:

1. The abstract says the disconnect "mirrors a well-documented crisis in psychology and health research" (line 73).
2. The intro opens by calling SE practice "characterized more by folklore, intuition, and contested conventional wisdom" (line 113)---an aggressive characterization of the field.
3. The intro's second paragraph calls the PL debate an illustration of "this crisis" (line 118).
4. Section 2.2 (`\subsubsection{The Methodological Reform in Psychology and Epidemiology}`) draws explicit parallels between SE and the psychology replication crisis, suggesting SE has the "same pattern" and needs the "same reform."
5. The Section 3 opener (line 311) states "psychology and epidemiology have undergone a methodological reform that SE has yet to experience"---implying SE is behind.

This framing risks:
- Alienating the SE community by implying the entire field's empirical work is methodologically deficient.
- Overclaiming that there is a "crisis" in SE comparable to psychology's replication crisis (which involved widespread failure to replicate).
- Obscuring the paper's actual contribution: Causal inference is not the goal for *all* empirical SE questions, but for a *specific class* of intervention-outcome questions it matters greatly.

---

## New Narrative Arc

### Core Insight to Convey

Causal inference per se is never the goal. The goal is understanding causal mechanisms. SE has always relied on descriptive, correlational, and qualitative evidence for theory proposition and mechanism explanation---and this has been productive. But there is a specific class of problems where these approaches are unsatisfying: **questions about whether specific interventions (code review, CI/CD, tool adoption, language choice) produce specific outcomes (fewer defects, higher productivity, better maintainability)**. For these questions:

1. Stakeholders (practitioners, managers, policymakers) *need* to know the causal effect to inform decisions.
2. Even when authors frame findings as correlational, downstream citations and the broader practitioner media read everything causally.
3. Without explicit identification strategies, contested findings lead to unproductive debates that cannot be resolved by more data or more regression controls.

### New Intro Structure (4--5 paragraphs)

**Paragraph 1 --- SE's empirical tradition is valuable but limited for a class of questions.**
- SE has built a rich empirical tradition: descriptive studies, correlational analyses, qualitative investigations, controlled experiments.
- This body of work has advanced our understanding of software development processes, team dynamics, and tool ecosystems.
- Yet a specific class of empirical questions---those about the causal effect of interventions on outcomes---remains difficult to answer convincingly with the field's dominant methodological tools.
- When practitioners ask whether adopting code review reduces defects, whether CI/CD improves release quality, or whether a typed language decreases bug rates, they are asking *causal* questions that demand more than correlational evidence.

**Paragraph 2 --- The problem: Intervention-outcome questions are everywhere, and current evidence is unsatisfying.**
- Many SE studies investigate questions of this kind, using observational data from software repositories.
- The dominant approach---large-scale regression analysis with covariate controls---can reveal associations but cannot distinguish genuine causal effects from selection biases and confounding.
- The problem is compounded downstream: Even when authors carefully qualify findings as correlational, practitioners, managers, and downstream papers often interpret them causally.
- Provide concrete examples: The PL-defect debate (Ray et al. -> Berger et al. controversy); tool adoption studies where results are read as evidence for/against adoption.
- In extreme cases this produces controversies that cannot be resolved by collecting more data or running more regressions, because the disagreement is about *identification*---the conditions under which the data can bear a causal interpretation.
- **Key nuance**: The issue is not that correlational evidence is "bad" but that for intervention-outcome questions, it is *insufficient* for the conclusions people actually draw from it.

**Paragraph 3 --- Causal inference methods offer a path forward for these specific questions.**
- Modern causal inference methods (developed in econometrics and epidemiology) provide principled approaches for exactly this class of problems.
- Their value lies in transparency: Every causal design rests on assumptions that are explicitly stated, examined, and debated.
- Brief mention of the credibility revolution and its relevance: Design-based methods (DiD, IV, RDD, panel FE) exploit features of the data structure to provide credible identification without requiring all confounders to be measured.
- These methods do not claim perfection; they insist on making assumptions visible so the research community can evaluate their plausibility.

**Paragraph 4 --- SE lacks an accessible introduction to this toolkit.**
- The SE community lacks a unified tutorial on these methods.
- Our analysis of 5,341 papers (ICSE, FSE, ASE, 2015--2025) shows that 29% of empirical SE papers investigate causal questions, but fewer than 4% employ causal inference methods (Section~\ref{sec:bg-adoption}).
- Recent methodological contributions have begun addressing specific gaps (cite Graf et al. on IV, omitted variable bias paper, causal DAGs for RE, Nocera et al. on matching), but no existing work spans the full toolkit.
- This tutorial fills that gap.

**Paragraph 5 --- Contributions (keep current structure, lightly revised).**
- Three contributions: primer, guide, worked examples.
- Same content as current, but adjust language to avoid "crisis" framing.

**Paragraph 6 --- Paper organization (keep as is).**

### New Abstract

Rewrite to:
- Remove the "mirrors a well-documented crisis in psychology" sentence.
- Replace with framing about intervention-outcome questions being a specific class of problems where current methods are insufficient.
- Keep all other content (primer, guide, worked examples).

---

## Section 2.2 --- Move to Appendix

### What to Move

The entire `\subsubsection{The Methodological Reform in Psychology and Epidemiology}` (lines 197--218) moves to a new appendix section, titled something like "The Methodological Reform in Psychology and Epidemiology" or "Parallels with Other Disciplines."

### What to Retain in the Main Text

The key references and insights from Section 2.2 should be woven into the new introduction narrative (Paragraph 2--3) and into Section 2.1 (bg-tutorials), rather than dropped entirely:

| Current Section 2.2 Point | Where It Goes |
|---|---|
| Hernán's "C-word" argument: avoiding causal language doesn't prevent causal interpretation, it just obscures assumptions | Intro Paragraph 2 (the downstream-interpretation problem) |
| Grosz's "taboo" finding: pushing causal reasoning underground impairs study design | Intro Paragraph 2 or 4 (briefly, to motivate the gap) |
| Haber et al.'s evidence that 52% of health abstracts imply causality despite associational language | Intro Paragraph 2 (parallel to SE's own pattern) |
| Rohrer's DAGs for psychology; Wysocki's collider bias warning | Keep in Section 2.1 (related work on tutorials/guides) or Section 3 primer |
| Lundberg's estimand-first principle | Keep in Section 2.1 or Section 4 guide |
| Lederer's editorial guidance | Keep in Discussion (FAQ about "why should I change?") |
| Rohrer 2024 tutorial as closest analog | Keep in Section 2.1 (related work) |
| Killingsworth-Rohrer income-happiness case study | Can be mentioned in intro briefly, or moved to appendix with Section 2.2 |

### Appendix Placement

- Add as a new appendix section (e.g., `\section{Parallels with Methodological Reform in Other Disciplines}` in the appendix).
- The appendix version can be almost verbatim from the current Section 2.2, with minor edits to adjust forward/backward references.
- Add a brief forward pointer from the intro or Section 2: "For a detailed discussion of parallel methodological reforms in psychology and epidemiology, see Appendix~X."

---

## Section 2 Restructuring

After the move, Section 2 becomes:

> **Section 2: Background and Related Work**
> 
> 2.1 Existing Tutorials and Methodological Guides in SE (keep, lightly expand with some 2.2 references)
> 2.2 The Development of the Causal Inference Toolkit (currently 2.2.1, promoted to 2.2)
> 2.3 Causal Inference Adoption in SE to Date (currently 2.3, keep as is)

The "Psychology and Epidemiology" section becomes an appendix. Section 2.2.1 (History of the toolkit) is promoted from subsubsection to subsection since it no longer has a sibling.

---

## Cross-Reference Updates

The following cross-references and language must be updated after the restructuring:

| Location | Current | New |
|---|---|---|
| Abstract (line 73) | "mirrors a well-documented crisis in psychology and health research" | Remove crisis analogy; reframe around intervention-outcome questions |
| Intro para 2 (line 118) | "illustrates this crisis" | "illustrates this challenge" or similar |
| Intro para 4 (line 131) | "the SE community lacks an accessible, unified introduction to this toolkit" | Keep but adjust preceding context |
| Section 2.3 (line 206) | "The SE community exhibits the same pattern, as we will show in Section~\ref{sec:bg-adoption}" | Remove or rewrite (this sentence is in the moved Section 2.2) |
| Section 2.3 Implications (line 225) | "a picture strikingly similar to the problems reported in psychology and epidemiology" | Soften or remove the comparison |
| Section 2.3 Implications (line 303) | "mirrors the pattern that Haber documented in health research and that Grosz described as a 'taboo' in psychology" | Rewrite to stand alone without the psychology parallel |
| Section 3 opener (line 311) | "psychology and epidemiology have undergone a methodological reform that SE has yet to experience" | Rewrite: focus on the toolkit's maturity and the gap in SE adoption |
| Section 3 (line 314) | "the textbooks listed in Section~\ref{sec:bg-causal-history}" | Update label if section numbering changes |
| Section 5 (line 606) | "see previous footnote in Section~\ref{sec:bg-adoption}" | Check if still valid |
| Discussion FAQ (line 1144) | "Psychology's replication crisis led to sweeping methodological reforms" | Keep but soften: present as an observation about other fields' trajectories, not as a direct analogy |
| Discussion FAQ (line 1147) | "Our analysis (Section~\ref{sec:bg-adoption}) shows..." | Keep, check ref still valid |

---

## Tone Calibration

Throughout the revisions, apply these tone guidelines:

- **Do say**: "For a specific class of questions---those about interventions and outcomes---the field's current methodological tools are insufficient."
- **Do say**: "Causal inference is not the goal for all empirical SE research, but for questions about whether an intervention produces an outcome, it is essential."
- **Do say**: "The challenge is not that SE studies are 'wrong' but that for intervention-outcome questions, correlational evidence cannot support the conclusions that stakeholders draw."
- **Don't say**: "crisis," "reform that SE has yet to experience," "SE exhibits the same pattern as psychology."
- **Don't say**: "folklore, intuition, and contested conventional wisdom" (as a characterization of the entire field).
- **Don't imply**: That all SE empirical work is methodologically deficient; the issue is specific to intervention-outcome questions.

---

## Actionable Tasks

- [ ] Rewrite the abstract (remove crisis analogy, reframe around intervention-outcome questions)
- [ ] Rewrite Intro Paragraph 1 (SE's empirical tradition is valuable but limited for a class of questions)
- [ ] Rewrite Intro Paragraph 2 (the intervention-outcome problem, with examples and the downstream-interpretation issue)
- [ ] Rewrite Intro Paragraph 3 (causal inference methods as a path forward for these questions)
- [ ] Revise Intro Paragraph 4 (SE lacks a tutorial; weave in key 2.2 references)
- [ ] Revise Intro Paragraph 5 (contributions --- adjust language, remove crisis framing)
- [ ] Move Section 2.2 (`\subsubsection{The Methodological Reform in Psychology and Epidemiology}`) to a new appendix section
- [ ] Promote Section 2.2.1 (History of the toolkit) from `\subsubsection` to `\subsection` and renumber
- [ ] Weave key Section 2.2 references into the intro and Section 2.1 per the table above
- [ ] Add a forward pointer from intro or Section 2 to the new appendix
- [ ] Revise Section 2.3 Implications paragraph to remove direct psychology parallels
- [ ] Revise Section 3 opening paragraph to remove "reform SE has yet to experience"
- [ ] Update Discussion FAQ (line 1144) to soften the psychology analogy
- [ ] Update all cross-references (`\ref`, `\label`) affected by section renumbering
- [ ] Full pass for remaining "crisis" / "reform" / "taboo" language in the paper
