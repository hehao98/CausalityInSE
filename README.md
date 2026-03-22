# Causal Inference for Empirical Software Engineering: A Tutorial

**Target Venue:** ACM Transactions on Software Engineering and Methodology (TOSEM)

**Status:** Drafting phase --- Sections 1--2 drafted; Section 3 primer under active planning and drafting.

## Repository Organization

- `paper/`: Contains the LaTeX source code and compiled PDF of the manuscript.
- `notebooks/`: Contains R Markdown notebooks used for data analysis (e.g., `literature_review.Rmd`).
- `data/`: A Git submodule pointing to the [CausalityInSE-Data](https://github.com/hehao98/CausalityInSE-Data) repository, which stores large datasets (e.g., `commits.csv.zip`, `se_papers_metadata.csv`).
  This separation prevents large files from bloating the main repository and causing issues with tools like Overleaf.

## Paper Vision

This tutorial paper aims to provide an accessible introduction to causal inference and causal claim assessment for software engineering researchers. Using the longstanding programming language vs. defect proneness debate as a worked example, the paper walks readers through:

1. The intellectual landscape of causal inference (potential outcomes, graphical causal models, design-based approaches) and why it matters for SE,
2. A four-step causal credibility assessment framework (derive causal theory -> define estimand and identifying assumptions -> acknowledge limitations -> navigate alternative explanations),
3. Two diagnostic-then-constructive worked examples showing the framework's power to both critically evaluate existing studies and guide improved designs:
   - **Example A (Ray et al.):** Diagnoses the identification failures in the landmark PL-defect study, then shows how panel fixed effects on the *same GitHub data* would have provided stronger identification by exploiting within-developer and within-repository variation.
   - **Example B (Bogner & Merkel):** Diagnoses the selection bias in a cross-sectional JavaScript vs. TypeScript comparison, then shows how the framework decomposes the compound "language" treatment into the sharper "type system adoption" question and redesigns the study as a TypeScript migration difference-in-differences on the *same GitHub data*.

The paper should be self-contained and pedagogically oriented so that an SE researcher with no prior exposure to causal inference can (a) understand the state of the art, (b) critically evaluate causal claims in existing work, and (c) apply the framework to their own research.

## Paper Structure

1. **Introduction** (Section 1) --- *Drafted.* Motivates the problem: SE practice is driven by folklore; empirical SE research produces voluminous but often inconclusive evidence because of its reliance on correlational methods. Causal inference offers a principled path forward. Three contributions: primer, four-step framework, two worked examples.

2. **Background & Related Work** (Section 2) --- *Drafted.* Three subsections:
   - 2.1 Existing tutorials and methodological guides in SE (positioning our contribution)
   - 2.2 The causal inference challenge in econometrics, psychology, and epidemiology (development of the toolkit; the methodological reform movement)
   - 2.3 Causal inference adoption in SE to date (empirical analysis of 5,341 papers from ICSE + FSE + ASE, 2015--2025; taxonomy and trend figures)

3. **A Primer on Causal Inference for SE Researchers** (Section 3) --- *Under active planning; see detailed plan below.*

4. **The Four-Step Causal Credibility Assessment Framework** (Section 4) --- *Drafted.*

5. **Worked Example A: The PL--Defect Debate** (Section 5) --- *Section 5.1 (PL debate review) drafted; Sections 5.2--5.4 TODO.*

6. **Worked Example B: TypeScript and Code Quality** (Section 6) --- *TODO.*

7. **Discussion** (Section 7) --- *TODO.*

8. **Conclusion** (Section 8) --- *TODO.*

---

## Task Backlog

### Phase 0: Literature Review and Framing (Completed)

- [x] LR1: Classify causal methods in top-venue SE papers; refine taxonomy and trend analysis for paper-ready figures
- [x] LR2: Conduct literature review on intellectual traditions of causal inference
- [x] LR3: Conduct literature review on the PL vs. defect proneness debate
- [x] LR4: Conduct literature review on parallel causal inference problems in psychology and health research
- [x] Synthesize findings from LR1--LR4 to finalize paper framing and contribution statement
- [x] Revise paper structure based on literature review findings

### Phase 1: Tutorial Drafting (Current Phase)

- [x] Write Introduction (Section 1)
- [x] Write Background & Related Work (Section 2), informed by LR1--LR4
- [ ] **Write the Causal Inference Primer (Section 3)**
  - [ ] Restructure Section 3 according to the detailed plan above
  - [ ] Write new Section 3.1: "What Does It Mean for X to Cause Y?" (conceptual perspectives, SE-grounded)
  - [ ] Revise Section 3.2: Consolidate correlation != causation and regression limitations; add DAG-informed regression pointer
  - [ ] Revise Section 3.3: Restructure as "Three Pillars" with sub-subsections for PO, DAGs, design-based identification; add SE examples for each method
  - [ ] Write new Section 3.4: "A Pragmatic Stance for SE Research" (potential outcomes for validity, DAGs for mechanisms, design-based identification when possible)
  - [ ] Write opening paragraph positioning Section 3 relative to Section 2 and scoping coverage
- [ ] Write the Four-Step Framework (Section 4) --- *currently drafted but may need revision after Section 3 is finalized*

### Phase 2: Worked Example A --- Ray et al. + Panel FE (Section 5)

- [x] Write the PL vs. defect proneness debate review (Section 5.1)
- [ ] Write diagnostic assessment of Ray et al. (Section 5.2): walk through all four steps showing identification failures
- [ ] Conduct and write up the downstream citation analysis (Section 5.3)
- [ ] Write constructive improvement narrative: how the framework guides from regression to panel FE (Section 5.4)
- [ ] Construct panel dataset from Ray et al.'s GitHub data (or comparable sample): identify polyglot developers and repositories
- [ ] Operationalize language assignment at the commit level; compute defect metrics
- [ ] Implement panel FE analysis; conduct specification tests and robustness checks
- [ ] Write up brief empirical demonstration (Section 5.5)

### Phase 3: Worked Example B --- Bogner & Merkel + TypeScript DiD (Section 6)

- [ ] Write diagnostic assessment of Bogner & Merkel 2022 (Section 6.1): walk through four steps showing selection bias
- [ ] Write the treatment decomposition narrative: from "language" to "type system adoption" (Section 6.2)
- [ ] Write constructive improvement narrative: redesign as TypeScript adoption DiD (Section 6.3)
- [ ] Identify TypeScript migration events in GitHub data (JS projects that adopted TS)
- [ ] Construct matched treatment-control sample of JS projects; compute pre/post defect metrics
- [ ] Implement DiD analysis with event-study plots and pre-trend tests
- [ ] Write up brief empirical demonstration (Section 6.4)
- [ ] Write synthesis of both examples: how the framework upgrades designs (Section 6.5)

### Phase 4: Integration and Submission

- [ ] Write Discussion (Section 7): implications for SE research practices, how both examples generalize, relationship to methodological reform efforts
- [ ] Write Conclusion (Section 8)
- [ ] Full paper revision and internal review
- [ ] Submit to TOSEM

## Key Risks and Open Questions

1. **Positioning relative to Furia et al. (2024):** They applied structural causal models (DAG-based adjustment) to coding competition data. Our contribution differs on three dimensions: (a) we provide a general tutorial framework, not just one application; (b) our Example A uses design-based identification (panel FE) rather than DAG-based adjustment; (c) our Example B uses a different identification strategy (DiD exploiting a natural experiment) on real-world project data. The two-example structure demonstrates that the framework generates *different* improved designs depending on the data structure and question.

2. **Scope management:** Two worked examples plus a tutorial primer is ambitious. The empirical demonstrations in Sections 5.4 and 6.4 should be brief and pedagogical (not full empirical papers) --- enough to show feasibility and illustrate the framework's output, not to definitively answer the causal questions.

3. **Empirical feasibility --- Example A (Panel FE):** Depends on sufficient within-developer language variation in the data. Mitigation: assess variation early; even a null or weak result is pedagogically valuable (it illustrates Step 3's honesty about limitations).

4. **Empirical feasibility --- Example B (TypeScript DiD):** Depends on identifying enough clean TypeScript migration events (JS projects that adopted TS) with comparable pure-JS controls. Mitigation: TypeScript adoption has been widespread since ~2017; initial scoping on GHArchive should reveal whether the sample is sufficient.

5. **Framing the contribution:** This is primarily a tutorial paper whose contribution is the framework and the demonstration of its diagnostic-then-constructive power. The empirical demonstrations are illustrations, not standalone empirical contributions. For TOSEM, a tutorial/survey paper category may be most appropriate.

6. **Audience calibration:** The paper must be accessible to SE researchers with no causal inference background while also being rigorous enough to satisfy methodologists. The two-example structure helps: Example A (regression -> panel FE) is a gentler step; Example B (cross-sectional -> DiD with treatment decomposition) shows the framework's full power.

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
