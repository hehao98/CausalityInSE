# Causal Inference for Empirical Software Engineering: A Tutorial

**Target Venue:** ACM Transactions on Software Engineering and Methodology (TOSEM)

**Status:** Drafting phase --- Sections 1--3 drafted; Section 4.1 (PL debate review) drafted; Sections 4.2--6 TODO.

## Repository Organization

- `paper/`: Contains the LaTeX source code and compiled PDF of the manuscript.
- `notebooks/`: Contains R Markdown notebooks used for data analysis (e.g., `literature_review.Rmd`).
- `data/`: A Git submodule pointing to the [CausalityInSE-Data](https://github.com/hehao98/CausalityInSE-Data) repository, which stores large datasets (e.g., `commits.csv.zip`, `se_papers_metadata.csv`).
  This separation prevents large files from bloating the main repository and causing issues with tools like Overleaf.

## Paper Vision

This tutorial paper aims to provide an accessible introduction to causal inference for software engineering researchers. The **programming language vs. code quality debate** serves as the paper's single unifying case study --- a three-decade-old controversy that has generated controlled experiments, landmark observational studies, high-profile reproductions, and widespread downstream misinterpretation, making it the ideal vehicle for demonstrating both the diagnostic and constructive power of causal inference methods.

The paper walks readers through:

1. The intellectual landscape of causal inference (potential outcomes, graphical causal models, design-based approaches) and why it matters for SE,
2. A pragmatic stance for conducting credible causal inquiry in SE, integrated into the primer (Section 3.4), which synthesizes the toolkit into actionable guidance: building on prior research and practitioner knowledge to propose causal theories, framing research designs as target trials, using DAGs to make assumptions explicit, exploiting quasi-experimental variation for identification, and honestly engaging with alternative explanations,
3. A **literature synthesis of the PL vs. code quality debate** (Section 4.1--4.2) that:
   - Traces the debate through three phases (controlled experiments → large-scale observational studies → reproduction and causal identification),
   - Documents the **downstream misinterpretation problem** using Ray et al. as a case study: quantitative citation analysis showing how hedged correlational findings are reinterpreted as causal claims in downstream papers, tech media, and practitioner discourse --- illustrating a systemic pattern that extends well beyond this single study,
   - Argues that the debate's impasse is fundamentally about **identification**, not data or statistics, and that resolving it requires the causal inference toolkit,
4. Two diagnostic-then-constructive **worked examples** (Sections 4.3--4.4), both drawn from the PL-quality debate, showing the pragmatic stance's power to both critically evaluate existing studies and guide improved designs:
   - **Example A (Ray et al.):** Diagnoses the identification failures in the landmark PL-defect study, then shows how panel fixed effects on the *same GitHub data* would have provided stronger identification by exploiting within-developer and within-repository variation.
   - **Example B (Bogner & Merkel):** Diagnoses the selection bias in a cross-sectional JavaScript vs. TypeScript comparison, decomposes the compound "language" treatment into the sharper "type system adoption" question, and redesigns the study as a TypeScript migration difference-in-differences on the *same GitHub data*.
5. An ACM Empirical Standard for Causal Inquiry in SE (appendix), providing a concrete, verifiable checklist for authors, reviewers, and editors.

The paper should be self-contained and pedagogically oriented so that an SE researcher with no prior exposure to causal inference can (a) understand the state of the art, (b) critically evaluate causal claims in existing work, and (c) apply the pragmatic stance to their own research.

## Paper Structure

1. **Introduction** (Section 1) --- *Drafted.* Motivates the problem and states contributions.
   - Opens with the richness of empirical SE (descriptive, correlational, qualitative, experimental) but identifies causal intervention-outcome questions as a specific class that the dominant approach (large-scale regression on observational data) cannot answer convincingly.
   - Uses the PL-quality debate as a motivating example: Ray et al.'s hedged correlational findings were widely cited as causal; Berger et al.'s reproduction showed the disagreement is about *identification*, not data or statistics.
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
   - Framing paragraph: chosen as unifying case study because it illustrates the full arc (contested findings, downstream misinterpretation, impasse that better statistics cannot resolve). Goal is not to resolve the debate but to retrospectively illustrate how the toolkit diagnoses and improves prior designs.
   - 4.1 Literature synthesis: three phases of PL-quality research --- *Drafted.*
     - **Phase 1 --- Controlled experiments**: Traded ecological validity for internal validity. Prechelt (2000): within-language individual differences exceed between-language differences (developer skill confounds language comparisons). Hanenberg et al. (2010--2014): isolated type system dimension via custom language with randomized assignment; static types benefit understanding unfamiliar code and fixing type-related errors but not semantic errors. Endrikat et al. (2014): types help most when documentation is poor---"language effect" is contingent on development context. Nanz & Furia (2015): Rosetta Code as quasi-experiment; compiled strongly typed languages less prone to runtime failures. Collective finding: static type systems help with a specific class of errors under specific conditions, with modest effect sizes relative to individual differences.
     - **Phase 2 --- Large-scale observational studies**: Shifted to repository mining; gained ecological validity but sacrificed identification. Bhattacharya & Neamtiu (2011): 4 C/C++ projects, confounds language with project characteristics. Bissyandé et al. (2013): 100K projects, treated correlations as informative without addressing endogeneity. Ray et al. (2014/2017): 729 GitHub projects, 17 languages, "modest but significant" association; hedged framing but widely cited as causal. Kochhar et al. (2016): independent replication corroborating associations, but replication of an association ≠ causal identification. Meyerovich & Rabkin (2013): language adoption driven by ecosystems/codebases/experience, not intrinsic features---language choice is endogenous. Gao et al. (2017): partially circumvented identification by annotating pre-fix JS code with TS types; type checkers detect ~15% of public bugs, holding project constant.
     - **Phase 3 --- Reproduction and toward causal identification**: Shifted from "what are the correlations?" to "can any correlational approach answer the causal question?" Berger et al. (2019): meticulous reproduction of Ray et al., reduced significant associations from 11 to 4 with exceedingly small effect sizes. Furia et al. (2022): Bayesian analysis showing project-specific characteristics dominate language effects. Furia et al. (2024): applied structural causal models to competition data, found "considerable differences between associational and causal analysis of the same data"---a smoking gun for the identification problem. Bogner & Merkel (2022): JS vs TS comparison finding better code quality but 60% higher bug-fix ratio for TS, consistent with selection bias. No existing study of real-world PL effects uses within-repository panel variation or design-based identification.
   - 4.2 The misinterpretation problem: when correlations become causal claims --- *Drafted.*
     - **Citation analysis**: 451 papers citing Ray et al. retrieved from Semantic Scholar; 339 with available full-text classified into four categories (causal/hedged/neutral/critical). Results: 24% causal framing, 12% hedged, 2% critical, 62% neutral/tangential. Among papers that engage with the PL-quality finding, causal interpretations outnumber hedged ones ~2:1---striking given that the original study never claims a causal relationship.
     - **Practitioner discourse**: Berger et al. noted people "misinterpreted [findings] as a causal relationship"; even the article reporting the debunking uses causal language in its headline. Blog posts rank languages by "bug-proneness" using causal verbs ("produce," "eliminate"). Hacker News commenters treat regression coefficients as switchable causal effects ("A Haskell project can expect to see 63% of the bug fixes that a C++ project would see").
     - **Implications**: Pattern matches Hernán's (2018) causal language problem and Grosz et al.'s (2020) documentation in psychology. Conventional defense (hedge more carefully) fails---24% causal framing despite explicit hedging, confirming Haber et al.'s finding that associational euphemisms do not prevent causal interpretation. The problem is not imprecise language but *absent identification*---without specifying causal estimand, confounding structure, or identification strategy, readers fill the gap with their priors, producing the 2:1 causal-to-hedged ratio. The pragmatic stance addresses this at the source by requiring researchers to state their causal question, draw their DAG, and argue for identification.
   - 4.3 Example A --- Diagnosing and improving Ray et al. (diagnostic assessment via pragmatic stance; constructive improvement via panel FE; brief empirical demonstration) --- *TODO.*
   - 4.4 Example B --- Diagnosing and improving Bogner & Merkel (diagnostic assessment; treatment decomposition from "language" to "type system adoption"; constructive improvement via TypeScript DiD; brief empirical demonstration) --- *TODO.*
   - 4.5 Synthesis: how the pragmatic stance upgrades research designs (connects both examples; shows different data structures → different improved designs) --- *TODO.*

5. **Discussion** (Section 5) --- *TODO.*

6. **Conclusion** (Section 6) --- *TODO.*

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

- [ ] Write diagnostic assessment of Ray et al. (Section 4.3): walk through pragmatic stance showing identification failures
- [ ] Write constructive improvement narrative: from regression to panel FE (Section 4.3)
- [ ] Construct panel dataset from Ray et al.'s GitHub data (or comparable sample)
- [ ] Implement panel FE analysis; conduct specification tests and robustness checks
- [ ] Write up brief empirical demonstration (Section 4.3)
- [ ] Write diagnostic assessment of Bogner & Merkel (Section 4.4): walk through pragmatic stance showing selection bias
- [ ] Write treatment decomposition: from "language" to "type system adoption" (Section 4.4)
- [ ] Write constructive improvement: redesign as TypeScript adoption DiD (Section 4.4)
- [ ] Identify TypeScript migration events; construct matched treatment-control sample
- [ ] Implement DiD analysis with event-study plots and pre-trend tests
- [ ] Write up brief empirical demonstration (Section 4.4)
  - *See `plans/20260331 - Example B TypeScript DiD Plan.md` for the detailed plan.*
- [ ] Write synthesis of both examples (Section 4.5): how the pragmatic stance generates different improved designs depending on data structure

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

4. **Empirical feasibility --- Example B (TypeScript DiD):** Depends on identifying enough clean TypeScript migration events (JS projects that adopted TS) with comparable pure-JS controls. Mitigation: TypeScript adoption has been widespread since ~2017; initial scoping on GHArchive should reveal whether the sample is sufficient.

5. **Literature synthesis and misinterpretation analysis:** The citation analysis of Ray et al.'s downstream impact needs to be rigorous enough to be convincing but scoped enough to remain a supporting argument rather than a standalone empirical contribution. A well-chosen sample (~50--100 citing papers) with clear classification criteria should suffice.

6. **Framing the contribution:** This is primarily a tutorial paper whose contribution is the primer (with its pragmatic stance and companion empirical standard) and the demonstration of its diagnostic-then-constructive power through the PL-quality debate. The literature synthesis and empirical demonstrations are illustrations, not standalone contributions. For TOSEM, a tutorial/survey paper category may be most appropriate.

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
