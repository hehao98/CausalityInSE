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

1. **Introduction** (Section 1) --- *Drafted.* Motivates the problem: SE's dominant approach (large-scale correlational analysis) cannot answer causal questions about interventions and outcomes; yet stakeholders routinely interpret findings causally. Causal inference offers transparency and principled identification. Three contributions: primer with pragmatic stance, literature synthesis of the PL-quality debate (with misinterpretation analysis), two worked examples.

2. **Background & Related Work** (Section 2) --- *Drafted.* Three subsections:
   - 2.1 Existing tutorials and methodological guides in SE (positioning our contribution)
   - 2.2 The causal inference toolkit: origins and scope (development of the toolkit across three intellectual traditions)
   - 2.3 Causal inference adoption in SE to date (empirical analysis of 5,341 papers from ICSE + FSE + ASE, 2015--2025; taxonomy and trend figures)

3. **A Primer on Causal Inference for SE Researchers** (Section 3) --- *Drafted.* Four subsections:
   - 3.1 What does it mean for X to cause Y? (four perspectives on causation)
   - 3.2 Why cannot we use descriptive and correlational evidence? (four failure modes)
   - 3.3 The causal inference toolkit (potential outcomes, DAGs, design-based identification)
   - 3.4 A pragmatic stance for SE research (synthesizes the toolkit into actionable guidance; incorporates the former "guide" section)

4. **The Programming Language and Code Quality Debate** (Section 4) --- *Unified section; Section 4.1 drafted, rest TODO.* Single umbrella theme housing the literature synthesis and both worked examples:
   - 4.1 Literature synthesis: three phases of PL-quality research (controlled experiments → observational studies → reproduction/causal identification) --- *Drafted.*
   - 4.2 The misinterpretation problem: when correlations become causal claims (quantitative citation analysis of Ray et al.; media and paper examples; why hedged language fails) --- *TODO; see plan.*
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
