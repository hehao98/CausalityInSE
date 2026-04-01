# Causal Inference for Empirical Software Engineering: A Tutorial

**Target Venue:** ACM Transactions on Software Engineering and Methodology (TOSEM)

**Status:** Drafting phase --- Sections 1--3 drafted; Section 4.1 (PL debate review) drafted; Sections 4.2--6 TODO.

## Repository Organization

- `paper/`: Contains the LaTeX source code and compiled PDF of the manuscript.
- `notebooks/`: Contains R Markdown notebooks used for data analysis (e.g., `literature_review.Rmd`).
- `data/`: A Git submodule pointing to the [CausalityInSE-Data](https://github.com/hehao98/CausalityInSE-Data) repository, which stores large datasets (e.g., `commits.csv.zip`, `se_papers_metadata.csv`).
  This separation prevents large files from bloating the main repository and causing issues with tools like Overleaf.

## Paper Vision

This tutorial paper aims to provide an accessible introduction to causal inference for software engineering researchers. The paper walks readers through:

1. The intellectual landscape of causal inference (potential outcomes, graphical causal models, design-based approaches) and why it matters for SE,
2. A pragmatic stance for conducting credible causal inquiry in SE, integrated into the primer (Section 3.4), which synthesizes the toolkit into actionable guidance: building on prior research and practitioner knowledge to propose causal theories, framing research designs as target trials, using DAGs to make assumptions explicit, exploiting quasi-experimental variation for identification, and honestly engaging with alternative explanations,
3. A **literature synthesis of the PL vs. code quality debate** (Section 4.1--4.2) that:
   - Traces the debate through three phases (controlled experiments → large-scale observational studies → reproduction and causal identification),
   - Documents the **downstream misinterpretation problem** using Ray et al. as a case study: quantitative citation analysis showing how appropriately hedged associational findings are reinterpreted as causal claims in downstream papers, tech media, and practitioner discourse --- illustrating a systemic field-level pattern (the absence of causal inference infrastructure) that extends well beyond this single study,
   - Argues that the debate's persistent impasse reflects two orthogonal challenges: **identification** (can the research design distinguish causal effects from confounding?) and **measurement** (are the outcomes and treatments valid proxies for the constructs of interest?). This paper addresses the identification dimension, showing how the causal inference toolkit can strengthen study designs; it acknowledges but does not claim to solve the measurement dimension (e.g., noisy bug-fix heuristics, ambiguous "language" treatments),
4. **Worked examples** demonstrating the pragmatic stance's diagnostic and constructive power through retrospective application of the toolkit to existing studies (see "Open Decision" below),
5. An ACM Empirical Standard for Causal Inquiry in SE (appendix), providing a concrete, verifiable checklist for authors, reviewers, and editors.

The paper should be self-contained and pedagogically oriented so that an SE researcher with no prior exposure to causal inference can (a) understand the state of the art, (b) critically evaluate causal claims in existing work, and (c) apply the pragmatic stance to their own research.

### Open Decision: Which Worked Examples?

Three candidate examples exist, each empirically analyzed in notebooks. The central tension is between **thematic unity** (keeping everything within the PL debate) vs. **pedagogical breadth** (showing the toolkit works across different data structures and domains). A secondary tension is how to frame the diagnostic vs. constructive arcs across two examples. See the detailed comparative assessment in "Which Examples Should the Paper Use?" below.

**The three candidates:**

- **Example A (Ray et al. panel FE):** Retrospectively applies panel FE to the landmark PL-defect study on the *same GitHub data*. Cross-sectional → panel upgrade. Most language-defect associations attenuate to non-significance under two-way FE; only C and Haskell survive. *Fully implemented, empirically compelling, no self-citation.*
- **Example B (Bogner & Merkel OVB + PSM/IPW):** Applies DAG-guided covariate selection, OVB diagnostics, PSM, and IPW to a cross-sectional JS vs. TS comparison. Shows that three estimators (OLS, PSM, IPW) converge on the same fragile estimate (−0.0065, −0.0060, −0.0065 for code smells), proving the estimator is not the bottleneck. *Fully implemented as a diagnostic example; no constructive counterpart needed (the lesson is precisely that cross-sectional methods hit a ceiling). No self-citation.*
- **Example C (Cursor AI ITS → DiD):** Strips the published DiD methodology from He et al. (MSR 2026) and shows what progressively weaker designs conclude. Naive ITS suggests Cursor *improves* code quality; repo FE *flips the sign* (quality worsens). *Diagnostic implemented, constructive exists in published paper; self-citation; different domain (AI coding tools).*

**The leading options (in order of preference):**

1. **B + C (diagnostic → constructive arc):** Example B systematically diagnoses why cross-sectional methods fail (DAG, OVB, PSM/IPW convergence → ceiling); Example C shows what works when longitudinal data is available (ITS → FE → sign-flip → DiD). Natural pedagogical arc: "this cannot work" → "here is what does." Demonstrates the widest range of methods. Self-citation with C is mitigated by B being the primary (third-party) example.
2. **A + C (cross-sectional vs. longitudinal):** The two examples illustrate structurally different data settings and both produce sign-flips/collapse under FE. The shared punchline is powerful. Requires restructuring Section 4.
3. **A + B (PL-debate-only):** Thematic unity within the PL debate; no self-citation. Example B now stands on its own as the diagnostic half (no risky DiD needed); Example A provides the constructive half.

## Paper Structure

1. **Introduction** (Section 1) --- *Drafted.* Motivates the problem and states contributions.
   - Opens with the richness of empirical SE (descriptive, correlational, qualitative, experimental) but identifies causal intervention-outcome questions as a specific class that the dominant approach (large-scale regression on observational data) cannot answer convincingly.
   - Uses the PL-quality debate as a motivating example: Ray et al. carefully presented associational findings, yet downstream papers and practitioners widely interpreted them as causal; Berger et al.'s reproduction highlighted both measurement concerns and the absence of causal identification. The debate's persistence reflects two orthogonal challenges --- identification and measurement --- and this paper addresses the former.
   - Argues that causal inference methods offer a path forward not through perfection but through *transparency*---every design rests on assumptions (parallel trends, exclusion restrictions) that can be stated, tested, and debated.
   - Documents the adoption gap: 29% of empirical SE papers ask causal questions, yet <4% use any causal method; design-based methods are virtually absent.
   - States three contributions: (1) self-contained primer with pragmatic stance, (2) literature synthesis of PL-quality debate with citation-analysis-based misinterpretation evidence, (3) two worked examples demonstrating the pragmatic stance's diagnostic-then-constructive power.
   - Provides a roadmap of the remaining sections.

2. **Background & Related Work** (Section 2) --- *Drafted.* Three subsections positioning the contribution and quantifying the gap.
   - 2.1 Existing tutorials and methodological guides in SE (positioning our contribution)
     - Acknowledges major SE methodological infrastructure (Wohlin textbook, ACM Empirical Standards, Robillard's threats-to-validity framing) but notes none addresses identification strategies, sensitivity analysis, or criteria for when correlational evidence can support causal claims.
     - Reviews diagnostic side: mapping studies (Siebert, Giamattei) found sparse use of Pearl's graphical framework; causal graph instability results (Hulse et al.) strengthen the case for theory-driven DAG construction.
     - Reviews prescriptive side: individual tutorials (IV by Graf et al., omitted variable bias, causal DAGs for RE, matching for MSR) each cover one method without integrating into the broader landscape.
     - Positions our contribution as the first integrative treatment spanning potential outcomes, graphical causal models, and design-based identification, with a pragmatic stance and companion empirical standard.
   - 2.2 The causal inference toolkit: origins and scope (development of the toolkit across three intellectual traditions)
     - Traces three intellectual traditions: statisticians (potential outcomes: Neyman, Rubin---define *what* to estimate), econometricians (credibility revolution: Angrist, Imbens, Card---shift from modeling to *research design*; 2021 Nobel Prize), computer scientists (Pearl's DAGs and do-calculus---encode *why* assumptions hold).
     - Notes the new generation of accessible textbooks (Angrist & Pischke, Cunningham, Hernán & Robins, Huntington-Klein) that made these methods available to non-specialists.
     - States the paper's integrative view: potential outcomes build foundations, design-based identification provides robust estimates, DAGs decompose mechanisms.
   - 2.3 Causal inference adoption in SE to date (empirical analysis of 5,341 papers from ICSE + FSE + ASE, 2015--2025; taxonomy and trend figures)
     - Corpus: 5,341 papers from ICSE, FSE, ASE (2015--2025); abstracts retrieved from Semantic Scholar/OpenAlex; classified by LLM along three dimensions (empirical, MSR, causal RQ/method).
     - The causal ambition--methodology gap: 2,136 empirical papers, 621 (29%) ask causal RQs, only 81 (3.8%) use causal methods; ratio has remained ~7:1 over the decade (structural, not transitional).
     - Method distribution: dominated by RCTs (37) and causal fault localization (17); regression-based causal inference (10) with no formal identification; design-based methods (DiD, IV, RDD, panel FE) nearly absent (<10 total).
     - Three implications: (1) large gap between conclusions stakeholders draw and what methods support, (2) SE's causal methods are overwhelmingly RCTs or fault localization, insufficient for observational questions, (3) design-based methods that powered the credibility revolution remain unexplored despite SE's natural panel data structure.

3. **A Primer on Causal Inference for SE Researchers** (Section 3) --- *Drafted.* Four subsections building from conceptual foundations to actionable guidance.
   - 3.1 What does it mean for X to cause Y? (four perspectives on causation)
     - Uses the TypeScript-defects question as a running example throughout.
     - Presents four complementary perspectives: (1) regular association (Hume)---fails because it cannot distinguish causal effects from selection; (2) counterfactual dependence (Lewis/Rubin)---precise but introduces the fundamental problem of causal inference (never observe both worlds); (3) intervention (Woodward/Pearl)---distinguishes *seeing* from *doing*, formalizes the gap between P(Y|X) and P(Y|do(X)); (4) target trial (Hernán)---most pragmatic, asks researcher to describe the hypothetical RCT and evaluate departures.
     - Synthesizes: counterfactual view yields *estimands*, interventionist view yields *identification conditions*, target trial view yields *research design*; together they form the backbone of the three technical pillars.
   - 3.2 Why cannot we use descriptive and correlational evidence? (four failure modes)
     - Motivates the toolkit by showing why the SE-dominant approach (group comparison + regression controls) fails for causal questions, using the TypeScript example.
     - Simple group comparison: teams choosing TypeScript differ systematically (more experienced, more disciplined)---confounders create association even with zero causal effect.
     - Four problems with regression controls: (1) *unobserved confounders*---regression can only adjust for measured variables; developer skill, team culture are unmeasurable from repository data; bias can be arbitrarily large. (2) *Collider bias*---conditioning on a common effect (e.g., popularity) creates spurious associations (Berkson's paradox). (3) *Mediator bias*---conditioning on variables on the causal pathway (e.g., tooling quality) attenuates the genuine effect. (4) *Reverse causality*---cross-sectional data cannot determine causal direction.
     - Concludes that regression *can* support causal claims under specific conditions, but determining those conditions requires the formal frameworks in the next subsection.
   - 3.3 The causal inference toolkit (potential outcomes, DAGs, design-based identification)
     - Frames the three pillars as answering three distinct questions: what to estimate (potential outcomes), what to assume (DAGs), how to make assumptions credible (design-based identification).
     - **3.3.1 Potential outcomes**: Formalizes counterfactual view. Binary treatment notation (Y_i(1), Y_i(0)); defines ATE, ATT, LATE, CATE as substantive choices. Derives identifying assumptions: RCT requires random assignment + SUTVA + compliance; selection-on-observables requires conditional ignorability + overlap. Notes sensitivity analysis tools (Rosenbaum bounds, coefficient stability, E-value, robustness value) to probe plausibility.
     - **3.3.2 Graphical causal models and DAGs**: Addresses which variables to condition on. Presents a PL-defect DAG (Figure 1) with confounders (domain, team skill, org culture, codebase age), mediators (type safety, tooling), and a collider (popularity). Explains back-door criterion: condition on common causes, *not* on mediators or colliders. Three limitations: require domain knowledge, depend on completeness, encode only qualitative structure.
     - **3.3.3 Design-based identification**: For settings where key confounders are unmeasurable. Presents four methods with SE examples: DiD (TypeScript migration; cites Fang et al., Chen et al., He et al.), IV (instrument affecting treatment only through treatment; cites Graf et al.), RDD (threshold-based assignment; no successful SE application known), panel FE (same developer across languages; absorbs time-invariant confounders; cites Cheng et al. at Google). Table summarizes methods, estimands, and identifying assumptions.
   - 3.4 A pragmatic stance for SE research (synthesizes the toolkit into actionable guidance)
     - **Build on prior research and practitioner knowledge**: Three sources of domain knowledge---prior quantitative studies (propose DAG edges), gray literature (practitioner causal beliefs), qualitative SE research (mechanistic accounts). Creates a virtuous cycle: prior work proposes structures, rigorous methods evaluate them, findings refine theory.
     - **Use counterfactual reasoning to frame research designs**: Articulate the target trial before analyzing data---what is the treatment, population, outcome, timing? Forces clarity on ambiguities (e.g., "language choice" = type system? ecosystem? community?).
     - **Use DAGs to reason about mechanisms and covariate selection**: Construct a DAG encoding assumed causal structure; apply back-door criterion; make every assumption explicit for reviewers to challenge specific edges.
     - **Use design-based identification when the setting permits**: When data contain temporal variation, staggered adoption, instruments, or thresholds, exploit these rather than relying solely on covariate adjustment. Table maps data features to methods. Different methods estimate different quantities.
     - **Iterate between question, assumptions, and design**: The process is iterative---DAG may reveal ill-defined treatment, estimand may constrain feasible strategies, discovering quasi-experimental variation may suggest sharper estimands.
     - **When clean identification is unavailable**: Use best available strategy, be transparent about limitations and direction of likely bias. Consider *reformulating* the question to exploit available variation (e.g., "Does language affect quality?" → "Does adopting a type system reduce defects?" amenable to DiD).
     - **Engage with alternative explanations**: Mitigate, don't just list. Three patterns: alternative mechanism (condition on mediator), unmeasured confounding (sensitivity analysis, falsification tests), reverse causality (panel data temporal signatures). SE-specific measurement challenges: noisy proxies, construct validity, SUTVA violations.
     - **Promises and perils of causal inference in SE**: Promises---SE data is inherently panel data; rich quasi-experimental variation from policies, staggered adoptions, migrations; rich prior literature for DAG construction. Perils---unmeasured confounders (skill, culture), compound treatments ("adopting TypeScript" bundles many things), SUTVA violations in interconnected ecosystems, noisy outcome proxies.

4. **The Programming Language and Code Quality Debate** (Section 4) --- *Unified section; Sections 4.1--4.2 drafted, rest TODO.* Single umbrella theme housing the literature synthesis and both worked examples.
   - Framing paragraph: chosen as unifying case study because it illustrates the full arc (associational findings, downstream causal misinterpretation, and a persistent impasse). The debate's persistence reflects two orthogonal challenges --- identification (which this paper addresses) and measurement (which it acknowledges but does not solve). Goal is not to resolve the debate or to criticize any prior study, but to retrospectively illustrate how the causal toolkit can strengthen the identification dimension of existing designs.
   - 4.1 Literature synthesis: three phases of PL-quality research --- *Drafted.*
     - **Phase 1 --- Controlled experiments**: Traded ecological validity for internal validity. Prechelt (2000): within-language individual differences exceed between-language differences (developer skill confounds language comparisons). Hanenberg et al. (2010--2014): isolated type system dimension via custom language with randomized assignment; static types benefit understanding unfamiliar code and fixing type-related errors but not semantic errors. Endrikat et al. (2014): types help most when documentation is poor---"language effect" is contingent on development context. Nanz & Furia (2015): Rosetta Code as quasi-experiment; compiled strongly typed languages less prone to runtime failures. Collective finding: static type systems help with a specific class of errors under specific conditions, with modest effect sizes relative to individual differences.
     - **Phase 2 --- Large-scale observational studies**: Shifted to repository mining; gained ecological validity but without the identification that randomization provides. Bhattacharya & Neamtiu (2011): 4 C/C++ projects; language and project characteristics are confounded in this design. Bissyandé et al. (2013): 100K projects, reporting correlations without addressing endogeneity. Ray et al. (2014/2017): 729 GitHub projects, 17 languages, reported a "modest but significant" association between language class and defect proneness; the authors appropriately framed their findings as associational, though the study was widely cited downstream as causal evidence. Kochhar et al. (2016): independent replication corroborating the associations, though replication of an association does not itself constitute causal identification since the same confounding structure operates across studies. Meyerovich & Rabkin (2013): showed language adoption is driven by ecosystems/codebases/experience, not intrinsic features---language choice is endogenous. Gao et al. (2017): partially circumvented the identification challenge by annotating pre-fix JS code with TS types; type checkers detect ~15% of public bugs, holding project constant.
     - **Phase 3 --- Reproduction and toward causal identification**: Shifted from "what are the correlations?" to "can any correlational approach answer the causal question?" Berger et al. (2019): meticulous reproduction of Ray et al., reduced significant associations from 11 to 4 with exceedingly small effect sizes. Furia et al. (2022): Bayesian analysis showing project-specific characteristics dominate language effects. Furia et al. (2024): applied structural causal models to competition data, found "considerable differences between associational and causal analysis of the same data"---a smoking gun for the identification problem. Bogner & Merkel (2022): JS vs TS comparison finding better code quality but 60% higher bug-fix ratio for TS, consistent with selection bias. No existing study of real-world PL effects uses within-repository panel variation or design-based identification.
   - 4.2 The misinterpretation problem: when correlations become causal claims --- *Drafted.*
     - **Citation analysis**: 451 papers citing Ray et al. retrieved from Semantic Scholar; 339 with available full-text classified into four categories (causal/hedged/neutral/critical). Results: 24% causal framing, 12% hedged, 2% critical, 62% neutral/tangential. Among papers that engage with the PL-quality finding, causal interpretations outnumber hedged ones ~2:1---striking given that Ray et al. themselves appropriately presented their findings as associational, not causal. The misinterpretation is a downstream phenomenon reflecting the field's lack of causal inference infrastructure, not any shortcoming of the original study.
     - **Practitioner discourse**: Berger et al. noted people "misinterpreted [findings] as a causal relationship"; even the article reporting the debunking uses causal language in its headline. Blog posts rank languages by "bug-proneness" using causal verbs ("produce," "eliminate"). Hacker News commenters treat regression coefficients as switchable causal effects ("A Haskell project can expect to see 63% of the bug fixes that a C++ project would see").
     - **Implications**: Pattern matches Hernán's (2018) causal language problem and Grosz et al.'s (2020) documentation in psychology. Conventional defense (hedge more carefully) fails---24% causal framing despite Ray et al.'s explicit and appropriate hedging, confirming Haber et al.'s finding that associational euphemisms do not prevent causal interpretation. The problem is not that any individual study uses imprecise language (Ray et al.'s language is careful), but that the field lacks the identification infrastructure to guide readers on *whether* a causal interpretation is warranted. The pragmatic stance addresses this structural gap by requiring researchers to state their causal question, draw their DAG, and argue for identification.
   - 4.3 Example A --- Applying the pragmatic stance to Ray et al. (retrospective application of the toolkit to show how panel FE on the same data strengthens identification; brief empirical demonstration) --- *TODO.*
   - 4.4 Example B --- Diagnosing Bogner & Merkel (DAG-guided covariate selection, OVB assessment under two specifications, PSM/IPW convergence demonstrating that the estimator is not the bottleneck; cross-sectional ceiling argument) --- *TODO (notebook analysis complete; narrative write-up needed).*
   - 4.5 Synthesis: how the pragmatic stance upgrades research designs (connects both examples; shows different data structures → different improved designs) --- *TODO.*

5. **Discussion** (Section 5) --- *TODO.*

6. **Conclusion** (Section 6) --- *TODO.*

## Current Empirical Results from Notebooks

This section summarizes the key results from the analysis notebooks, assesses their compellingness, and discusses whether both worked examples should be retained.

### Example A: Panel Fixed Effects on Ray et al.'s Data

**Notebooks:** `notebooks/toplas19_reanalysis.Rmd` (main panel FE analysis) and `notebooks/toplas19_bootstraping.Rmd` (measurement error sensitivity analysis).

**Story.** The notebook takes the same commit-level dataset from Ray et al. (2014) / Berger et al. (2019) — a landmark large-scale empirical study that appropriately reported associational findings — and retrospectively applies panel fixed effects to demonstrate how the causal toolkit can strengthen identification on the same data:

| Model | Unit of analysis | Fixed effects | N obs | Key result |
|-------|-----------------|---------------|-------|------------|
| M1 (Ray 2014) | Repository | None | 728 | 11 significant language coefficients |
| M2 (Berger 2019) | Repo-Language | None | 1,039 | Broadly similar; replication at repo-language level |
| M3 | Repo-Language | Repository | 552 | Most effects attenuate; only C++ remains significant (but halved) |
| M4 | Developer-Language | Developer | 13,370 | Further attenuation; C++ drops from 0.23 to 0.065 |
| M5 | Dev-Repo-Language | Developer + Repository (two-way) | 21,185 | **Most effects vanish**; only C and Haskell survive |

**Key coefficient trajectories** (zero-sum contrasts, FDR-adjusted significance):

- **C++**: 0.23\*\*\* (M1) → 0.256\*\*\* (M2) → 0.128\*\*\* (M3, repo FE) → 0.065\*\* (M4, dev FE) → **0.035 n.s.** (M5, two-way FE). The strongest "more defect-prone" language in the original study becomes insignificant once developer and repository confounders are absorbed.
- **Clojure**: −0.29\*\*\* (M1) → −0.277\*\*\* (M2) → −0.026 n.s. (M3) → −0.041 n.s. (M4) → **−0.002 n.s.** (M5). Completely vanishes.
- **Scala**: −0.28\*\*\* (M1) → −0.217\*\*\* (M2) → −0.004 n.s. (M3) → −0.016 n.s. (M4) → **0.025 n.s.** (M5). Completely vanishes.
- **Python**: 0.10\*\* (M1) → 0.104\* (M2) → −0.019 n.s. (M3) → 0.014 n.s. (M4) → **−0.031 n.s.** (M5). Vanishes.
- **Haskell**: −0.23\*\*\* (M1) → −0.203\*\*\* (M2) → −0.113 n.s. (M3) → −0.152\*\* (M4) → **−0.183\*\*\*** (M5). The *only* language whose effect *survives and strengthens* under two-way FE. This is interpretable: Haskell's pure functional paradigm with strong static typing may genuinely reduce certain classes of defects, and the FE identification provides stronger evidence than the cross-sectional analysis ever could.
- **C**: 0.15\*\*\* (M1) → 0.139\*\* (M2) → 0.070 n.s. (M3) → 0.116\*\*\* (M4) → **0.110\*** (M5). Survives, consistent with C's well-documented memory-safety vulnerabilities being a genuine language property rather than a developer or project artifact.

**Measurement error sensitivity** (bootstrapping notebook): Berger et al. (2019) documented a 36% false positive and 11% false negative rate in the keyword-based bug-fix labeling heuristic. The bootstrapping notebook perturbs labels accordingly:
- M1 (Berger-style bootstrap, 100K draws): Only C++, Clojure, Haskell remain robust (significant in ≥95% of draws).
- M5 (MC sensitivity, 1K draws, no resampling): Only **C and Haskell** remain robust. C++ drops to 19.4%, Clojure to 1.2%, Scala to ~0%. This confirms the two-way FE finding: measurement noise interacts with the already-attenuated coefficients to eliminate nearly all effects.

**Assessment: Highly compelling.** This example delivers exactly what the paper promises — the same data, a stronger identification strategy, substantially different results. Importantly, this is not a critique of Ray et al., who appropriately presented their findings as associational. Rather, it demonstrates what the field can learn by retrospectively applying causal methods: the cross-sectional associations reflected a mix of genuine language properties and confounding from unobserved developer and project characteristics. The progressive attenuation from M1 to M5 illustrates this decomposition, and the fact that two languages (Haskell, C) survive with interpretable coefficients makes the result more nuanced than a simple "everything vanishes." The measurement error analysis adds a second dimension of robustness. This example is ready for the paper once the narrative write-up is done.

### Example B: Diagnostic Assessment of Bogner & Merkel's JS vs. TS Comparison

**Notebook:** `notebooks/msr22_reanalysis.Rmd` (four-stage diagnostic with PSM/IPW; DiD not yet implemented).

**Story.** The notebook implements a four-stage progressive diagnostic of Bogner & Merkel (MSR 2022), showing *why* their cross-sectional JS vs. TS comparison cannot support causal conclusions — and demonstrating that switching to more sophisticated estimators does not solve the problem:

**Stage 1 — Replication, covariate balance, and DAG-guided covariate selection.** Replicates the original descriptive finding (TS has fewer code smells and lower cognitive complexity but 60% higher bug-fix ratio). Documents severe covariate imbalance between JS and TS repos (standardized mean differences: nLOC 0.06, commits 0.17, stars 0.40, creation year 0.75). A DAG-guided covariate selection exercise classifies each variable's causal role for code quality outcomes: `creation_year` and `framework` are confounders, `log_ncloc` is a confounder with minor post-treatment ambiguity, `log_commits` is post-treatment, and `log_stars` has both confounder and collider components (conditioning on it risks Berkson's paradox).

**Stage 2 — DAG-justified vs. kitchen-sink OLS and OVB assessment.** Compares two specifications:
- *M_dag (DAG-justified)*: `is_ts ~ log_ncloc + creation_year + framework` — only defensible confounders.
- *M_all (kitchen-sink)*: adds `log_commits + log_stars` — includes post-treatment and collider variables.

Key finding: Conditioning on stars attenuates the code smells coefficient by 32% (−0.0065 → −0.0044) and halves the robustness value (14.1% → 8.9%), consistent with collider bias. Three independent OVB diagnostics converge:
- *Coefficient instability*: The coefficient moves substantially as controls are added, with a DAG-justified zone (defensible) and a kitchen-sink zone (biased) separated visually.
- *Cinelli & Hazlett robustness values*: Small RVs under both specifications — a confounder as strong as project size could plausibly explain away the remaining effect. The kitchen-sink specification *weakens* robustness rather than strengthening it.
- *Oster proportional selection bounds*: δ\* values indicate fragility — unobservables need only be a fraction as important as observables to drive the coefficient to zero.

**Stage 3 — PSM and IPW: The estimator is not the bottleneck.** Implements propensity score matching (1:1 nearest-neighbor via MatchIt) and inverse probability weighting under the DAG-justified covariates. Three estimators converge on nearly identical results:

| Method | Code smells coef | SE | p | RV (point=0) |
|--------|-----------------|------|-------|-------------|
| OLS (M_dag) | −0.0065 | 0.0016 | 0.0001 | 14.1% |
| PSM (1:1 NN) | −0.0060 | 0.0017 | 0.0003 | 12.8% |
| IPW (ATT) | −0.0065 | 0.0022 | 0.003 | — |

The pattern repeats for cognitive complexity (−0.146, −0.143, −0.148) and bug-fix ratio (+0.059, +0.060, +0.065). Matching does not materially improve robustness values (14.1% → 12.8% for code smells; 19.4% → 18.5% for complexity). The IPW effective sample size is only 129 of 299 JS controls, confirming overlap problems. This is the strongest possible demonstration that the binding constraint is unobserved confounding, not the choice of statistical method.

**Stage 4 — The ceiling of cross-sectional data.** Argues that no amount of cross-sectional controls or estimator switching can separate "strict typing improves quality" from "high-quality teams write strict TypeScript." Within-project temporal variation (DiD on migration events) is needed.

**Appendix A — Treatment decomposition via `any`-type density.** Reframes the treatment from "JS vs. TS" to type-strictness intensity within TS repos. Improves covariate balance but no outcomes reach significance (N=305 TS repos). Included for completeness rather than as a central argument.

**Assessment: Strong diagnostic demonstration, still missing constructive counterpart.** The four-stage progression now covers the full diagnostic toolkit — DAG-guided covariate selection, OVB diagnostics, and the "three estimators, same answer" demonstration — making it one of the most thorough cross-sectional diagnostic case studies in the causal inference tutorial literature. The PSM/IPW convergence result is a pedagogically powerful lesson that many SE researchers need to learn: matching is not a magic fix for unobserved confounding. However, **the constructive counterpart (the TypeScript migration DiD) has not been implemented**, so Example B currently only shows what is *wrong* with existing designs without demonstrating what a *better* design produces. This limits its standalone value but makes it an excellent complement to Example A (which provides the constructive arc) or Example C (which shows the sign-flip under FE).

### Example C: Revisiting the Cursor AI Adoption Study (He et al., MSR 2026)

**Notebook:** `notebooks/msr26_reanalysis.Rmd` (descriptive pre-post and interrupted time series analysis).

**Context.** He et al. (MSR 2026), "Speed at the Cost of Quality: How Cursor AI Increases Short-Term Velocity and Long-Term Complexity in Open-Source Projects," studied the causal impact of Cursor AI adoption on development velocity and code quality using a staggered DiD design with matched controls. This reanalysis notebook strips away the DiD methodology and asks: What would you conclude from progressively weaker designs applied to the treated-repos-only panel data?

**Story.** The notebook uses monthly panel data (4,563 repo-months, ±6 months around Cursor adoption) for repos that adopted Cursor, examining five outcomes: commits, lines added, quality warnings, duplicated lines density, and cognitive complexity. All outcomes are log-transformed. The analysis progresses through two stages: a raw pre-post comparison, then an interrupted time series (ITS) across four model specifications.

**Raw pre-post comparison** (N=1,265 pre, 3,298 post observations):
- Commits: +8.1% (p=0.002), Lines Added: +14.4% (p<0.001) — velocity increases.
- Quality Warnings: +2.0% (p=0.39 n.s.), Duplicated Lines: +2.0% (p=0.38 n.s.) — no significant quality change in raw means.
- Cognitive Complexity: +5.7% (p<0.001) — complexity increases.

The raw comparison already hints at the velocity-quality trade-off, but the quality signal is weak and mixed. The ITS models reveal why.

**Interrupted Time Series (ITS) across four specifications.** The ITS decomposes the post-adoption trajectory into a level shift (immediate jump at adoption) and a slope change (trend after adoption), estimated across four model specifications: (1) no covariates, no FE; (2) with covariates (age, nLOC, contributors, stars, issues), no FE; (3) repo FE only; (4) repo FE + covariates.

| Outcome | Level (no FE) | Level (Repo FE+Cov) | Post slope (no FE) | Post slope (Repo FE+Cov) |
|---------|---------------|----------------------|---------------------|--------------------------|
| Commits | +0.49\*\*\* | +0.38\*\*\* | −0.17\*\*\* | −0.14\*\*\* |
| Lines Added | +1.39\*\*\* | +0.92\*\*\* | −0.42\*\*\* | −0.31\*\*\* |
| Quality Warnings | **−0.54\*\*\*** | **+0.065\*** | +0.27\*\*\* | +0.05\*\*\* |
| Duplicated Lines | −0.13\* | +0.017 n.s. | +0.046\* | −0.014 n.s. |
| Cognitive Complexity | **−0.33\*\*** | **+0.103\*\*\*** | +0.17\*\*\* | +0.045\*\*\* |

**Key patterns:**

- *Velocity outcomes (commits, lines added)*: Large, highly significant positive level shift at adoption — repos immediately start producing more commits and more lines of code. But the negative post-slope indicates the boost fades over subsequent months. This pattern is robust across all four specifications: the direction and significance do not change with or without FE, though effect sizes attenuate somewhat. The velocity story is straightforward and not confounded.

- *Quality outcomes — the sign flips under FE*: This is the central result. In naive models without repo FE:
  - Quality Warnings show a **negative** level shift (−0.54\*\*\*) — adoption appears to *reduce* quality warnings.
  - Cognitive Complexity shows a **negative** level shift (−0.33\*\*) — adoption appears to *reduce* complexity.
  
  A naive analyst would conclude: "Cursor adoption improves code quality." But with Repo FE (which absorbs all time-invariant repo characteristics):
  - Quality Warnings show a **positive** level shift (+0.065\*) — adoption actually *increases* quality warnings within the same repo.
  - Cognitive Complexity shows a **positive** level shift (+0.103\*\*\*) — adoption actually *increases* complexity within the same repo.
  
  **The sign has flipped.** The naive model gets the direction of the quality effect *exactly backwards*.

- *Why the sign flips — selection into treatment*: The explanation is selection bias. Repos that adopted Cursor early were systematically higher-quality to begin with — they had fewer quality warnings and lower complexity at baseline, likely because better-maintained projects with more active developers are the ones that adopt new AI tools. The naive model (without FE) confounds this baseline quality difference with the treatment effect: it compares post-adoption observations (which come from high-quality repos) against pre-adoption observations (which include a mix), making adoption *look* beneficial. Repo FE removes this confounding by comparing each repo against *its own* pre-adoption baseline, revealing that quality actually deteriorated within-repo after adoption.

- *Consistency with the published DiD*: The FE-corrected ITS direction (velocity up, quality down) matches the published MSR 2026 DiD results, which used matched control repos and a staggered adoption design. This convergence between the within-repo ITS and the full DiD provides triangulation: both designs point to the same conclusion, strengthening confidence in the causal interpretation.

- *What the ITS still cannot do*: Even with Repo FE, the treated-only ITS cannot distinguish the Cursor effect from secular time trends (e.g., repos naturally accumulating complexity as they age). This is precisely why the published paper uses a control group — the DiD differences out any time trends shared by treated and control repos. The progression from naive ITS → FE-corrected ITS → full DiD illustrates the pragmatic stance in action: each step addresses a specific threat (selection bias, then time trends), and the researcher must honestly assess which threats remain.

**Assessment: Highly compelling as a pedagogical demonstration.**

The sign-flip on quality outcomes is arguably the single most dramatic empirical result across all three candidate examples. It concretely illustrates Simpson's paradox in a real SE dataset — the kind of vivid, counterintuitive finding that readers remember and that motivates learning the toolkit. The velocity results (robust across specifications) provide a useful contrast: not every coefficient flips, and the difference between "robust to FE" and "flipped by FE" itself teaches readers how to interpret specification sensitivity.

The main limitations are: (1) the constructive counterpart (full DiD) lives in the published paper rather than being reimplemented in the tutorial, (2) it introduces a second domain beyond the PL-quality debate, and (3) it is the author's own paper. These are manageable — see the comparative assessment below.

### Which Examples Should the Paper Use?

Four candidate examples exist (three primary, one companion). The choice depends on how the paper frames its worked examples.

#### Candidate Summaries

| Dimension | Example A (Ray et al. Panel FE) | Example B (Bogner & Merkel OVB + PSM/IPW) | Example C (Cursor AI ITS → DiD) |
|-----------|---|----|---|
| Data structure | Cross-sectional (repos × languages) | Cross-sectional (JS vs. TS repos) | Longitudinal (repo-months around adoption) |
| Diagnostic story | Strong: progressive attenuation across 5 models | Strong: DAG-guided covariate selection + 3 OVB methods + 3 estimators converge | Strong: sign-flip under FE |
| Constructive counterpart | **Complete**: panel FE implemented | **None needed**: diagnostic-only by design (shows the ceiling of cross-sectional methods) | **External**: full DiD lives in published MSR 2026 paper |
| Pedagogical novelty | Shows coefficient attenuation (most effects vanish) | Shows DAG matters for covariate selection; OLS/PSM/IPW converge (estimator ≠ bottleneck); OVB fragility | Shows sign-flip (Simpson's paradox: quality appears to *improve* without FE, *worsens* with FE) |
| Methods demonstrated | Panel FE | DAG-guided covariate selection, OVB sensitivity analysis (sensemakr, Oster), PSM, IPW | ITS → DiD |
| Implementation status | Ready | **Ready** (all four stages implemented with actual results) | Diagnostic ready; constructive available from published paper |
| Self-citation risk | No (third-party study) | No (third-party study) | Yes (author's own paper) |

**What changed with Example B:** The notebook now implements a complete four-stage diagnostic arc including PSM and IPW (Stage 3), producing the "three estimators, same fragile answer" result. This eliminates the previous dependency on an unimplemented TypeScript DiD. Example B is now self-contained as a *diagnostic* example --- it does not need a constructive counterpart because its lesson is precisely that no selection-on-observables method can solve the identification problem. The constructive lesson ("you need longitudinal data") is delivered narratively in Stage 4, setting up Example A or C to demonstrate what a better design looks like.

#### Option 1: A + C (Cross-Sectional vs. Longitudinal)

**Framing:** Two examples illustrate *structurally different* data settings — a cross-sectional study and a longitudinal pre-post study — and show that both lead to qualitatively wrong conclusions when analyzed naively.

- **Example A (cross-sectional):** Panel FE on Ray et al.'s data absorbs confounders; most associations attenuate to non-significance.
- **Example C (longitudinal):** Repo FE on Cursor ITS *flips the sign* on quality outcomes from positive to negative.

**Pros:** Both empirically complete; dramatically different mechanisms (attenuation vs. sign-flip) deliver the same lesson; broadest reader engagement (PL debate + LLM tools); strongest demonstration of generality. **Cons:** Self-citation with Cursor; breaks single-theme framing; Example B's rich diagnostic material (DAG reasoning, PSM/IPW convergence) is lost or must be folded into the primer.

#### Option 2: B + C (Diagnostic Toolkit Showcase + Design-Based Identification)

**Framing:** The two examples demonstrate *complementary phases* of the pragmatic stance. Example B shows *diagnostic discipline* — how to systematically evaluate a cross-sectional claim using DAGs, OVB sensitivity analysis, and multiple estimators, arriving at the conclusion that cross-sectional data cannot support causal claims regardless of the estimator. Example C shows *constructive discipline* — how panel data and within-unit variation (repo FE, DiD) can overcome the limitations that Example B diagnoses.

- **Example B (diagnostic):** The Bogner & Merkel reanalysis demonstrates the full diagnostic arc: DAG-guided covariate selection reveals that "control for everything" is not innocuous (collider bias attenuates the coefficient by 32%); three OVB methods converge on fragility; OLS, PSM, and IPW produce identical estimates (−0.0065, −0.0060, −0.0065 for code smells), proving the estimator is not the bottleneck. The punchline: all selection-on-observables methods hit the same ceiling.
- **Example C (constructive):** The Cursor reanalysis demonstrates what happens when you have longitudinal data and can apply within-unit identification. Naive ITS suggests Cursor *improves* code quality; repo FE *flips the sign*. The progression from naive → FE → full DiD (in the published paper) shows exactly the kind of design upgrade that Example B argues is necessary.

**The pedagogical arc:** Example B establishes *why* cross-sectional methods fail (regardless of estimator sophistication), creating the motivation for the design-based methods that Example C demonstrates. Together, they walk the reader through the full pragmatic stance: diagnose → recognize the ceiling → redesign.

**Pros:**
- Natural narrative arc: B says "this cannot work" → C says "here is what does work." The reader follows the same journey they would in their own research.
- Example B is now empirically complete as a diagnostic example — no unfinished DiD needed. Its value lies in the *process* of diagnosis, not in a constructive fix.
- The B+C pairing covers the widest range of methods: DAG reasoning, OVB diagnostics (sensemakr, Oster), PSM, IPW (all from B) plus ITS, FE, DiD (all from C). No other pairing demonstrates as many methods.
- Both PL-quality and AI-tools domains are covered, demonstrating generality.
- The PSM/IPW convergence result in B ("matching does not fix unobserved confounding") is a lesson many SE researchers specifically need and is lost in the A+C pairing.
- Self-citation with Cursor is mitigated by B being the primary diagnostic example (third-party study); C is positioned as the constructive complement.

**Cons:**
- Self-citation (Example C). Same mitigation as Option 1.
- Example A's "coefficient attenuation across 5 models" narrative is arguably the single most dramatic demonstration in the set. Losing it weakens the paper's empirical impact.
- Without Example A, the paper loses the direct connection to the PL debate's central study (Ray et al.), which is the subject of the literature synthesis in Sections 4.1--4.2. This creates a narrative gap: Sections 4.1--4.2 discuss Ray et al. at length, but the worked example does not apply the toolkit to it.

#### Option 3: A + B as Companion Pair (PL-Debate-Only, No Self-Citation)

**Framing:** Both examples stay within the PL-quality debate. Example B serves as the cross-sectional diagnostic (showing the ceiling), Example A delivers the constructive upgrade (panel FE on the same domain).

- **Example B**: Full diagnostic arc on Bogner & Merkel — DAG, OVB, PSM/IPW convergence → "cross-sectional data cannot answer this question."
- **Example A**: Panel FE on Ray et al. → "with longitudinal data and within-unit variation, most effects vanish and two survive."

**The pedagogical arc:** B diagnoses the cross-sectional problem; A shows that panel data + FE can solve it within the same domain.

**Pros:** Thematic unity (everything stays in PL-quality); no self-citation; Example B is now strong enough to stand on its own as the diagnostic half; Example A provides the constructive half. **Cons:** Both are in the same narrow domain (PL-quality); readers from other SE subfields may find this less relevant; loses the dramatic sign-flip from Example C.

#### Option 4: A + C with B as Primer Illustration

Same as Option 1, but the Bogner & Merkel OVB diagnostics and PSM/IPW convergence result are folded into the primer (Section 3.2 or 3.4) as a worked illustration of sensitivity analysis and the "same assumption, same ceiling" lesson. This preserves Example B's pedagogical value without requiring a full Section 4.4.

**Pros:** Best of both worlds — A+C for the main examples plus B's material in the primer. **Cons:** The primer becomes longer and more empirical, which may disrupt its flow.

#### Option 5: A Only (Single Deep Worked Example)

**Framing:** The paper concentrates its entire worked example on one deeply developed demonstration — retrospectively applying the toolkit to Ray et al.'s PL-quality study — and uses the freed space for a richer primer, deeper literature synthesis, or an expanded discussion.

**Why this is a serious option:**
- **Example A is self-sufficient as a demonstration.** It already shows the full arc: naive cross-sectional regression → panel FE → most effects vanish → two survive with interpretable coefficients → measurement error sensitivity confirms robustness. The progressive attenuation across five models is a complete pedagogical story. Adding a second example provides breadth but is not necessary for the paper's claims.
- **One deep example > two shallow examples.** With only one example, the paper can: (a) walk through the pragmatic stance step-by-step in detail (target trial, DAG, identification, alternative explanations) rather than rushing through two; (b) include richer specification tests and robustness checks; (c) devote more space to the primer and discussion sections, which are the paper's primary contribution.

**Pros:** Eliminates all empirical risk. Allows deeper treatment of the primer and discussion. The paper's contribution (the primer with pragmatic stance) does not depend on the number of examples — one compelling demonstration suffices. **Cons:** Loses the "different data structures → different designs" demonstration. The paper's empirical section is narrower. Reviewers may ask "does this generalize beyond one study?"

**Mitigation for the "generalizability" concern:** The paper can note that the pragmatic stance has already been applied in published SE work — citing He et al. (MSR 2026) for DiD, Cheng et al. (FSE 2022) for panel FE at Google, and Furia et al. (TOSEM 2024) for structural causal models — without needing to reimplement each as a worked example.

#### Updated Recommendation

The five options in order of preference:

1. **Option 2 (B + C)** if comfortable with self-citation. The natural diagnostic→constructive arc is pedagogically the strongest framing; B is now complete as a diagnostic example; the widest range of methods is demonstrated (DAG, OVB, PSM, IPW, ITS, FE, DiD). The main cost is losing Example A's dramatic attenuation story and its connection to the Ray et al. literature synthesis.
2. **Option 1 (A + C)** if wanting the most dramatic empirical results. Both examples deliver sign-flips or collapse-to-insignificance; broadest reader engagement. Loses B's rich diagnostic material unless folded into the primer (Option 4).
3. **Option 4 (A + C with B as primer illustration)** if the paper can accommodate the space. Gets the best of all three examples but makes the primer longer.
4. **Option 3 (A + B)** for thematic unity within the PL debate and no self-citation. Example B no longer requires a risky DiD — it stands on its own as the diagnostic half.
5. **Option 5 (A only)** if wanting to minimize scope and maximize depth. Safest; frees space for the primer. The paper's contribution stands on the toolkit, not the number of examples.

**Appendices:**
- Historical development of causal inference and parallels with psychology/epidemiology --- *Drafted.*
- Frequently Asked Questions (27 Q&A pairs across 5 categories) --- *Drafted.*
- An Empirical Standard for Causal Inquiry in SE --- *Drafted.* Full ACM SIGSOFT Empirical Standards format (Application, Specific Attributes, Quality Criteria, Acceptable Deviations, Antipatterns, Invalid Criticisms, Suggested Readings, Exemplars).

---

## Task Backlog

### Phase 0: Literature Review and Framing (Completed)

- [x] LR1: Classify causal methods in top-venue SE papers; refine taxonomy and trend analysis for paper-ready figures
- [x] LR2: Conduct literature review on intellectual traditions of causal inference
- [x] LR3: Conduct literature review on the PL vs. defect proneness debate
- [x] LR4: Conduct literature review on parallel causal inference problems in psychology and health research
- [x] Synthesize findings from LR1--LR4 to finalize paper framing and contribution statement
- [x] Revise paper structure based on literature review findings

### Phase 1: Tutorial Drafting (Completed)

- [x] Write Introduction (Section 1)
- [x] Write Background & Related Work (Section 2), informed by LR1--LR4
- [x] Write the Causal Inference Primer (Section 3)
- [x] Merge Section 4 (Guide) into Section 3.4 (Pragmatic Stance)
- [x] Draft the ACM Empirical Standard for Causal Inquiry appendix
- [x] Draft the PL vs. defect proneness debate review (Section 4.1)

### Phase 2: PL vs. Code Quality Literature Synthesis (Section 4.1--4.2) --- Current Phase

- [ ] Expand Section 4.1 literature synthesis: broaden beyond the three-phase narrative to include more PL-quality literature and connect both papers' contexts --- *see `plans/20260327 - PL Code Quality Literature Synthesis.md`*
- [ ] Write Section 4.2 --- The Misinterpretation Problem:
  - [ ] Conduct quantitative citation analysis of Ray et al. (sample citing papers; classify causal vs. correlational interpretation)
  - [ ] Collect classic misinterpretation examples from tech media and practitioner discourse
  - [ ] Collect misinterpretation examples from downstream SE papers
  - [ ] Write the narrative tying citation analysis, media, and paper examples into a systemic pattern
  - [ ] Connect to Hernán (2018) causal language problem and the methodological reform literature

### Phase 3: Worked Examples (Sections 4.3--4.5)

- [ ] Write retrospective application of pragmatic stance to Ray et al. (Section 4.3): walk through how the toolkit suggests stronger identification on the same data
- [ ] Write constructive improvement narrative: from regression to panel FE (Section 4.3)
- [ ] Construct panel dataset from Ray et al.'s GitHub data (or comparable sample)
- [ ] Implement panel FE analysis; conduct specification tests and robustness checks
- [ ] Write up brief empirical demonstration (Section 4.3)
- [ ] Write diagnostic assessment of Bogner & Merkel (Section 4.4): walk through pragmatic stance showing DAG-guided covariate selection, OVB fragility, and PSM/IPW convergence
  - *Notebook analysis complete (`notebooks/msr22_reanalysis.Rmd`); see `plans/20260331 - Example B TypeScript DiD Plan.md` and `plans/20260401 - MSR22 Matching IPW Synthetic Control Plan.md` for detailed plans.*
- [ ] Write synthesis of both examples (Section 4.5): how the pragmatic stance generates different improved designs depending on data structure
- [ ] If using Example C (Cursor AI ITS → DiD): implement composition bias deep dive and restructure the `msr26_reanalysis.Rmd` notebook to follow a layered-reveal narrative --- *see `plans/20260331 - Cursor Example Composition Bias Deep Dive.md`*

### Phase 4: Integration and Submission

- [ ] Write Discussion (Section 5)
- [ ] Write Conclusion (Section 6)
- [ ] Revise Introduction and Abstract to reflect final structure
- [ ] Full paper revision and internal review
- [ ] Submit to TOSEM

## Key Risks and Open Questions

1. **Positioning relative to Furia et al. (2024):** They applied structural causal models (DAG-based adjustment) to coding competition data. Our contribution differs on three dimensions: (a) we provide a general tutorial with a pragmatic stance, not just one application; (b) our Example A uses design-based identification (panel FE) rather than DAG-based adjustment; (c) our Example B uses a different identification strategy (DiD exploiting a natural experiment) on real-world project data. The two-example structure demonstrates that the pragmatic stance generates *different* improved designs depending on the data structure and question.

2. **Scope management:** A literature synthesis + two worked examples + a tutorial primer is ambitious. The empirical demonstrations in Sections 4.3 and 4.4 should be brief and pedagogical (not full empirical papers) --- enough to show feasibility and illustrate the framework's output, not to definitively answer the causal questions.

3. **Empirical feasibility --- Example A (Panel FE):** Depends on sufficient within-developer language variation in the data. Mitigation: assess variation early; even a null or weak result is pedagogically valuable (it illustrates the pragmatic stance's honesty about limitations).

4. **Empirical feasibility --- Example B (resolved):** Example B no longer depends on an unimplemented TypeScript DiD. The notebook now implements a complete four-stage diagnostic (DAG-guided covariate selection, OVB assessment, PSM/IPW convergence, cross-sectional ceiling argument). It stands on its own as a diagnostic example.

5. **Literature synthesis and misinterpretation analysis:** The citation analysis documenting downstream causal interpretations of Ray et al.'s associational findings needs to be rigorous enough to be convincing but scoped enough to remain a supporting argument. The analysis documents a systemic field-level pattern (the absence of identification infrastructure leads to causal overinterpretation), not any shortcoming of the original study. A well-chosen sample (~50--100 citing papers) with clear classification criteria should suffice.

6. **Framing the contribution:** This is primarily a tutorial paper whose contribution is the primer (with its pragmatic stance and companion empirical standard) and the demonstration of its diagnostic-then-constructive power through the PL-quality debate. The literature synthesis and empirical demonstrations are illustrations, not standalone contributions. For TOSEM, a tutorial/survey paper category may be most appropriate. The paper addresses the **identification** dimension of empirical SE controversies and explicitly acknowledges that **measurement** (construct validity, noisy proxies, ambiguous treatments) is an equally important but orthogonal challenge that the causal toolkit does not solve.

7. **Audience calibration:** The paper must be accessible to SE researchers with no causal inference background while also being rigorous enough to satisfy methodologists. The unified PL-quality debate helps: the literature synthesis provides accessible context, Example A (regression → panel FE) is a gentler step, and Example B (cross-sectional → DiD with treatment decomposition) shows the pragmatic stance's full power.

## References (Key)

- Ray, D., Posnett, D., Filkov, V., & Devanbu, P. (2014). A Large Scale Study of Programming Languages and Code Quality in GitHub. FSE 2014.
- Ray, D., Posnett, D., Filkov, V., & Devanbu, P. (2017). A Large-Scale Study of Programming Languages and Code Quality in GitHub. CACM 2017.
- Berger, E. D., Hollenbeck, C., Maj, P., Vitek, O., & Vitek, J. (2019). On the Impact of Programming Languages on Code Quality. TOPLAS 2019.
- Furia, C. A., Torchiano, M., & Tempero, E. (2024). Structural causal models analysis of PL and defects. TOSEM 2024.
- Pearl, J. (2009). Causality: Models, Reasoning, and Inference. Cambridge University Press.
- Rubin, D. B. (1974). Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies. Journal of Educational Psychology.
- Angrist, J. D., & Pischke, J.-S. (2009). Mostly Harmless Econometrics. Princeton University Press.
- Cunningham, S. (2021). Causal Inference: The Mixtape. Yale University Press.
- Hernan, M. A., & Robins, J. M. (2020). Causal Inference: What If. Chapman & Hall/CRC.
- Rosenbaum, P. R. (2002). Observational Studies. Springer.
- Hill, A. B. (1965). The Environment and Disease: Association or Causation? Proceedings of the Royal Society of Medicine.
- Woodward, J. (2003). Making Things Happen: A Theory of Causal Explanation. Oxford University Press.
- Lewis, D. (1973). Causation. Journal of Philosophy.
- Holland, P. W. (1986). Statistics and Causal Inference. Journal of the American Statistical Association.
- Lundberg, I., Johnson, R., & Stewart, B. M. (2021). What Is Your Estimand? Defining the Target Quantity Connects Statistical Evidence to Theory. American Sociological Review.
- Imbens, G. W. (2020). Potential Outcome and Directed Acyclic Graph Approaches to Causality. Journal of Marketing Research.
