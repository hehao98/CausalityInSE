# Section 5: Discussion and Conclusion — Draft Plan

**Created:** 2026-04-15
**Status:** Drafted (2026-04-15)

## Overview

Section 5 closes the paper by distilling the tutorial's key messages into actionable implications for different audiences, reflecting on what the worked example reveals about the field, and acknowledging scope and limitations. The section should be concise (roughly 2–3 pages) and avoid recapitulating the primer or worked example in detail.

## Proposed Structure

### 5.1 — What the Worked Example Teaches Us

- [x] **The magnitude of design-driven shrinkage.** The progression from +911% (naive) → +158% (kitchen-sink) → +101% (DAG-justified) → +52% (CS DiD) → +32% (Borusyak DiD) is the paper's most visceral argument. Each step removes a specific, named source of bias. The discussion should frame this not as a curiosity of the AI-tools question but as a general warning: cross-sectional MSR studies that ask causal questions but rely on snapshot regressions may overstate effects by an order of magnitude. How many published SE findings would shrink similarly under design-based identification?
- [x] **Temporal collapse as a systemic MSR problem.** The temporal DAG (Section 4.1) revealed that cross-sectional GitHub API snapshots destroy the temporal ordering required for principled covariate selection—confounders and colliders become indistinguishable. This is not specific to AI tools; it applies to virtually every MSR study that queries the GitHub API once and throws everything into a regression. Recommend that MSR researchers invest in constructing longitudinal datasets (mining git histories, using GHArchive time series) rather than relying on atemporal snapshots.
- [x] **The substantive AI finding.** While framed as pedagogical, the 32–52% ATT for systematic AI tool adoption on monthly commits is timely and substantive. Briefly interpret: this estimates the effect of the *entire bundle* (AI tools + workflow reorganization + team self-selection into structured adoption), not the isolated effect of AI code generation. Parallel trends are supported but not proven; the estimate is conservative due to control-group contamination (individual AI use is unobservable). Position as a credible first estimate that future work can refine with richer treatment definitions or complementary identification strategies.

### 5.2 — Implications for the SE Community

- [x] **For reviewers and editors.** When a paper poses an intervention-outcome RQ, reviewers should require an explicit discussion of the extent to which the evidence supports a causal claim and the assumptions under which it does so. A regression coefficient presented as "the effect of X on Y" without identification argument is not a causal finding. Reviewers should use the empirical standard (Appendix D) as a checklist. Encourage editorial boards to formally adopt the standard into the ACM SIGSOFT Empirical Standards collection, following the precedent of Lederer et al.'s editor-endorsed guidance in epidemiology (Appendix B).
- [x] **For researchers.** Clear pointers for learning: Cunningham (2021) for design-based methods, Huntington-Klein (2021) for DAGs and research design, Hernán & Robins (2020) for the target trial framework, Angrist & Pischke (2009) for the formal potential outcomes treatment. Cross-reference the FAQ (Appendix C) for software tools and the empirical standard (Appendix D) for a workflow checklist. Emphasize the iterative nature of causal inquiry: the first identification strategy will have gaps; revision is the norm, not the exception.
- [x] **For data miners / MSR practitioners.** Actionable data-collection advice: construct panel datasets, record adoption timing, collect pre-treatment covariate snapshots, and preserve temporal ordering. These investments pay dividends far beyond any single study by enabling design-based identification that cross-sectional snapshots cannot support.

### 5.3 — SE's Comparative Advantages for Causal Inference

- [x] **SE data is inherently panel data.** Repositories have temporal structure, developers contribute across projects over time, and tools/practices are adopted in staggered fashion—making DiD, panel FE, and synthetic control designs natural fits. SE has the data infrastructure (version control histories, public repositories, platform traces, observable adoption events) that economists or epidemiologists often cannot access.
- [x] **Rich quasi-experimental variation.** Platform policies (e.g., GitHub Actions rollout, npm security mandates, language deprecation), company mandates, and ecosystem-wide shocks create exogenous variation that resembles natural experiments. The field is rich in settings where design-based identification is feasible—it simply hasn't been exploited.
- [x] **Reframing the narrative.** The message is not "SE is behind" but "SE has untapped potential." The tutorial provides the conceptual vocabulary; SE researchers have the data and domain expertise to apply it.

### 5.4 — The Qualitative–Quantitative Bridge

- [x] **Causal frameworks elevate qualitative research.** DAG construction requires domain knowledge that comes from qualitative research, practitioner accounts, gray literature, and prior quantitative studies (Section 3.4). The causal inference framework does not marginalize qualitative SE research—it makes explicit the essential role domain knowledge plays in proposing causal structures. Interviews, case studies, and practitioner postmortems become the theory-generating engine that quantitative designs then test.
- [x] **A virtuous cycle.** Prior qualitative/quantitative work proposes causal structures → rigorous designs evaluate them → findings refine theory → next iteration. Emphasize that this cycle is already implicit in much SE research; the toolkit makes it explicit and productive.

### 5.5 — Limitations and Scope

- [x] **Superficial adoption risk.** Raising empirical standards cannot prevent the superficial or ritualistic adoption of methods—applying DiD without understanding parallel trends, or drawing a DAG without genuine engagement with the causal structure. This echoes the grounded theory adoption problem in SE, where the method's label is adopted but its disciplined reasoning is not. The antidote is peer review informed by the empirical standard (Appendix D) and a culture of substantive engagement with identification assumptions.
- [x] **Specification searching with the new toolkit.** Adopting causal methods does not immunize against researcher degrees of freedom. Researchers can search across instrument choices, control group definitions, parallel trends windows, or covariate sets. Pre-registration of identification strategies (listed as "extraordinary" in Appendix D) and transparent reporting of all specifications tried are complementary safeguards.
- [x] **Compound treatments and SUTVA as open frontiers.** The paper identifies compound treatments (Section 4.1) and SUTVA violations (Section 3.4) as SE-specific challenges but does not resolve them. These are genuine research frontiers: adapting interference models to software dependency graphs and developer mobility networks, developing decomposition strategies for bundled interventions, and connecting to the growing literature on causal inference under network interference. SE-specific methodological contributions here could flow *back* to the broader causal inference community.
- [x] **Measurement validity as the parallel challenge.** Even as the community improves identification, corresponding investment in measurement validity—construct definition, proxy validation, triangulating outcome measures—is essential. A perfectly identified design with a bad outcome proxy still produces misleading conclusions. Identification and measurement are orthogonal challenges that both demand attention.
- [x] **Scope of the tutorial.** This tutorial focuses on the most widely applicable methods (selection-on-observables, DiD, panel FE); it does not cover ML-based causal inference (causal forests, double ML), causal discovery, or mediation analysis in depth. These are important extensions that build on—but do not replace—the identification foundations covered here.

### 5.6 — Concluding Paragraph

- [x] **From cumulative local estimates to general causal knowledge.** No single study resolves a causal question. The field builds general knowledge through triangulation: accumulating credible local estimates across complementary designs, data sources, and populations—just as economics built its evidence base on minimum wage effects or returns to education through dozens of independent, credible studies. SE's diversity of ecosystems (languages, platforms, team structures, cultures) makes it well suited to this strategy.
- [x] **Closing vision.** The causal inference toolkit's greatest contribution is not a specific method but a way of thinking: making assumptions transparent and open to scrutiny so that the strength of evidence is clearly communicated and the field can iteratively develop stronger designs. We envision this adoption bringing productive advancements on a broad range of important intervention-outcome questions—from the effect of AI coding tools to the impact of development practices, governance structures, and ecosystem policies—moving the field from the refrain of "correlation does not imply causation" toward the constructive discipline of "under what assumptions does this evidence support a causal interpretation?"

## Writing Guidelines

- **Length target:** ~2–3 pages (roughly 1,500–2,000 words).
- **Tone:** Forward-looking and constructive, not prescriptive or condescending. Acknowledge that descriptive and qualitative research remains indispensable; the call to action is specifically for the 29% of studies that ask causal questions.
- **Cross-references:** Anchor each point to the specific section, figure, or table in the paper that motivates it (e.g., Table 7 for the shrinkage progression, Figure 5 for temporal DAG, Appendix D for the empirical standard).
- **Avoid:** Recapitulating the primer or worked example in detail. Each paragraph should add new insight or implication, not summarize what was already said.
