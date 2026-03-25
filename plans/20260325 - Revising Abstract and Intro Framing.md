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


| Current Section 2.2 Point                                                                                                | Where It Goes                                                              |
| ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Hernán's "C-word" argument: avoiding causal language doesn't prevent causal interpretation, it just obscures assumptions | Intro Paragraph 2 (the downstream-interpretation problem)                  |
| Grosz's "taboo" finding: pushing causal reasoning underground impairs study design                                       | Intro Paragraph 2 or 4 (briefly, to motivate the gap)                      |
| Haber et al.'s evidence that 52% of health abstracts imply causality despite associational language                      | Intro Paragraph 2 (parallel to SE's own pattern)                           |
| Rohrer's DAGs for psychology; Wysocki's collider bias warning                                                            | Keep in Section 2.1 (related work on tutorials/guides) or Section 3 primer |
| Lundberg's estimand-first principle                                                                                      | Keep in Section 2.1 or Section 4 guide                                     |
| Lederer's editorial guidance                                                                                             | Keep in Discussion (FAQ about "why should I change?")                      |
| Rohrer 2024 tutorial as closest analog                                                                                   | Keep in Section 2.1 (related work)                                         |
| Killingsworth-Rohrer income-happiness case study                                                                         | Can be mentioned in intro briefly, or moved to appendix with Section 2.2   |


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


| Location                            | Current                                                                                                            | New                                                                                                  |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Abstract (line 73)                  | "mirrors a well-documented crisis in psychology and health research"                                               | Remove crisis analogy; reframe around intervention-outcome questions                                 |
| Intro para 2 (line 118)             | "illustrates this crisis"                                                                                          | "illustrates this challenge" or similar                                                              |
| Intro para 4 (line 131)             | "the SE community lacks an accessible, unified introduction to this toolkit"                                       | Keep but adjust preceding context                                                                    |
| Section 2.3 (line 206)              | "The SE community exhibits the same pattern, as we will show in Section~\ref{sec:bg-adoption}"                     | Remove or rewrite (this sentence is in the moved Section 2.2)                                        |
| Section 2.3 Implications (line 225) | "a picture strikingly similar to the problems reported in psychology and epidemiology"                             | Soften or remove the comparison                                                                      |
| Section 2.3 Implications (line 303) | "mirrors the pattern that Haber documented in health research and that Grosz described as a 'taboo' in psychology" | Rewrite to stand alone without the psychology parallel                                               |
| Section 3 opener (line 311)         | "psychology and epidemiology have undergone a methodological reform that SE has yet to experience"                 | Rewrite: focus on the toolkit's maturity and the gap in SE adoption                                  |
| Section 3 (line 314)                | "the textbooks listed in Section~\ref{sec:bg-causal-history}"                                                      | Update label if section numbering changes                                                            |
| Section 5 (line 606)                | "see previous footnote in Section~\ref{sec:bg-adoption}"                                                           | Check if still valid                                                                                 |
| Discussion FAQ (line 1144)          | "Psychology's replication crisis led to sweeping methodological reforms"                                           | Keep but soften: present as an observation about other fields' trajectories, not as a direct analogy |
| Discussion FAQ (line 1147)          | "Our analysis (Section~\ref{sec:bg-adoption}) shows..."                                                            | Keep, check ref still valid                                                                          |


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

## Citations

### New Citations to Add to `references.bib`

The revised intro needs concrete examples of well-known SE studies where intervention-outcome questions are answered with correlational evidence and findings get interpreted causally. The current paper already uses the PL-defect debate (Ray et al.) as the primary example. We should add one or two more from different SE domains.

**1. McIntosh, Kamei, Adams, Hassan (2016) --- Code review → software quality**

A widely-cited MSR study whose title ("The Impact of Modern Code Review Practices on Software Quality") uses causal language, but the analysis is correlational (regression with controls). Practitioners routinely cite this as evidence that code review *causes* quality improvements. Perfect example for Intro Paragraph 2.

```bibtex
@article{DBLP:journals/ese/McIntoshKAH16,
  author       = {Shane McIntosh and
                  Yasutaka Kamei and
                  Bram Adams and
                  Ahmed E. Hassan},
  title        = {An empirical study of the impact of modern code review
                  practices on software quality},
  journal      = {Empir. Softw. Eng.},
  volume       = {21},
  number       = {5},
  pages        = {2146--2189},
  year         = {2016},
  doi          = {10.1007/s10664-015-9381-9}
}
```

- DBLP key: `DBLP:journals/ese/McIntoshKAH16` (verify when DBLP recovers from current outage)
- **Use in intro**: Cite alongside the PL debate as a second example of an intervention-outcome question answered correlationally.

**2. Vasilescu, Yu, Wang, Devanbu, Filkov (2015) --- CI → quality and productivity**

Classic FSE study on CI adoption and quality/productivity outcomes. Correlational MSR design.

```bibtex
@inproceedings{DBLP:conf/sigsoft/VasilescuYWDF15,
  author       = {Bogdan Vasilescu and
                  Yue Yu and
                  Huaimin Wang and
                  Premkumar T. Devanbu and
                  Vladimir Filkov},
  title        = {Quality and productivity outcomes relating to continuous
                  integration in {GitHub}},
  booktitle    = {Proceedings of the 10th Joint Meeting on Foundations of
                  Software Engineering, {ESEC/FSE} 2015, Bergamo, Italy,
                  August 30--September 4, 2015},
  pages        = {805--816},
  publisher    = {{ACM}},
  year         = {2015},
  doi          = {10.1145/2786805.2786850}
}
```

- DBLP key: `DBLP:conf/sigsoft/VasilescuYWDF15` (verify when DBLP recovers)
- **Note**: Vasilescu is a co-author of this tutorial. Consider using **Hilton et al. (2016)** below as an alternative to avoid self-citation concerns. Authors should decide.

**3. (Alternative) Hilton, Tunnell, Huang, Marinov, Dig (2016) --- CI usage, costs, benefits**

Alternative CI example with no co-author overlap with the tutorial.

```bibtex
@inproceedings{DBLP:conf/kbse/HiltonTHMD16,
  author       = {Michael Hilton and
                  Timothy Tunnell and
                  Kai Huang and
                  Darko Marinov and
                  Danny Dig},
  title        = {Usage, costs, and benefits of continuous integration in
                  open-source projects},
  booktitle    = {Proceedings of the 31st {IEEE/ACM} International Conference
                  on Automated Software Engineering, {ASE} 2016, Singapore,
                  September 3--7, 2016},
  pages        = {426--437},
  publisher    = {{ACM}},
  year         = {2016},
  doi          = {10.1145/2970276.2970358}
}
```

- DBLP key: `DBLP:conf/kbse/HiltonTHMD16` (verify when DBLP recovers)
- **Use in intro**: Alternative to Vasilescu et al. for the CI example if self-citation is a concern.

### Existing Citations and Their Role in the New Framing

The following citations are already in `references.bib` and serve specific roles in the new narrative. No new bib entries needed for these.

| Citation | Key | Role in New Intro |
|---|---|---|
| Hernán (2018) "The C-Word" | `hernan2018cword` | **Paragraph 2**: Avoiding causal language does not prevent causal interpretation; it merely obscures assumptions. Supports the "downstream causal reading" argument. |
| Grosz et al. (2020) "Taboo" | `grosz2020taboo` | **Paragraph 2 or 4** (brief): The norm against causal language pushes causal reasoning underground, impairing study design. Use lightly, without implying SE has the same "taboo." |
| Haber et al. (2022) | `haber2022causal` | **Paragraph 2** (brief): 52% of health research abstracts imply causality despite associational language---a parallel pattern, mentioned as context, not as a direct SE indictment. |
| Devanbu et al. (2016) "Belief & Evidence" | `DBLP:conf/icse/Devanbu0B16` | **Paragraph 1**: SE practitioners hold strong beliefs about practices; empirical evidence is needed to inform decisions. |
| Forsgren et al. (2021) SPACE | `DBLP:journals/queue/ForsgrenSMZHB21` | **Paragraph 1 or 2**: Decision-making about developer productivity requires understanding causal effects of interventions. |
| Angrist & Pischke (2010) | `angrist2010credibility` | **Paragraph 3**: Brief mention of the credibility revolution. |
| Ray et al. (2014) + Berger et al. (2019) + rebuttals | `DBLP:conf/sigsoft/RayPFD14`, `DBLP:journals/toplas/BergerHMVV19`, `DBLP:journals/corr/abs-1911-11894` | **Paragraph 2**: Primary running example of an intervention-outcome controversy that correlational methods cannot resolve. |
| Rohrer (2024) tutorial for psychologists | `rohrer2024causal` | **Section 2.1** (related work): Closest analog to our tutorial, but limited to psychology and does not cover design-based identification. |

### Citations NOT Needed

The following were considered but are unnecessary:

- **Kitchenham et al. (2004) EBSE**: The evidence-based SE framing is tangential; our intro is about causal identification, not systematic reviews.
- **Stol & Fitzgerald on research methods**: Too broad; existing methodological citations suffice.
- **Fucci et al. (2017) on TDD**: An experimental study, not the observational-correlational pattern we are illustrating.

---

## Actionable Tasks

- Add new citations to `references.bib`: McIntosh et al. (2016) and one CI paper (Vasilescu et al. or Hilton et al.; authors decide)
- Verify all new DBLP keys against DBLP when the server recovers from current outage
- Rewrite the abstract (remove crisis analogy, reframe around intervention-outcome questions)
- Rewrite Intro Paragraph 1 (SE's empirical tradition is valuable but limited for a class of questions)
- Rewrite Intro Paragraph 2 (the intervention-outcome problem, with examples and the downstream-interpretation issue)
- Rewrite Intro Paragraph 3 (causal inference methods as a path forward for these questions)
- Revise Intro Paragraph 4 (SE lacks a tutorial; weave in key 2.2 references)
- Revise Intro Paragraph 5 (contributions --- adjust language, remove crisis framing)
- Move Section 2.2 (`\subsubsection{The Methodological Reform in Psychology and Epidemiology}`) to a new appendix section
- Promote Section 2.2.1 (History of the toolkit) from `\subsubsection` to `\subsection` and renumber
- Weave key Section 2.2 references into the intro and Section 2.1 per the table above
- Add a forward pointer from intro or Section 2 to the new appendix
- Revise Section 2.3 Implications paragraph to remove direct psychology parallels
- Revise Section 3 opening paragraph to remove "reform SE has yet to experience"
- Update Discussion FAQ (line 1144) to soften the psychology analogy
- Update all cross-references (`\ref`, `\label`) affected by section renumbering
- Full pass for remaining "crisis" / "reform" / "taboo" language in the paper

