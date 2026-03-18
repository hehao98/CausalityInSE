# Causal Inference for Software Engineering: A Tutorial

**Target Venue:** ACM Transactions on Software Engineering and Methodology (TOSEM)

**Status:** Planning phase — literature review and framing in progress.

## Paper Vision

This tutorial paper aims to provide an accessible introduction to causal inference and causal claim assessment for software engineering researchers. Using the longstanding programming language vs. defect proneness debate as a worked example, the paper walks readers through:

1. The intellectual landscape of causal inference (potential outcomes, graphical causal models, design-based approaches) and why it matters for SE,
2. A four-step causal credibility assessment framework (derive causal theory → define estimand and identifying assumptions → acknowledge limitations → navigate alternative explanations),
3. A diagnostic application of the framework to an existing, widely-known SE debate (Ray et al. 2014 and subsequent controversy), and
4. A constructive demonstration showing how the framework guides the design of improved studies (panel fixed effects analysis exploiting within-developer and within-repository variation).

The paper should be self-contained and pedagogically oriented so that an SE researcher with no prior exposure to causal inference can (a) understand the state of the art, (b) critically evaluate causal claims in existing work, and (c) apply the framework to their own research.

## Planned Paper Structure (Tentative)

1. **Introduction** — Motivate the problem: SE practice is driven by folklore and contested conventional wisdom; empirical SE research produces voluminous but often inconclusive evidence because of methodological limitations (descriptive/correlational evidence, qualitative opinion synthesis). Causal inference offers a principled path forward.

2. **Background & Related Work**
   - 2.1 Existing tutorials and methodological guides in SE (positioning our contribution)
   - 2.2 The intellectual traditions of causal inference (from Snow and the early formalization by Neyman, Fisher, and Rubin through the graphical causal models of Pearl, the design-based credibility revolution, and modern sensitivity analysis)
   - 2.3 Causal inference adoption in SE to date — *empirical analysis of top-venue SE papers (ASE + FSE + ICSE, 2015–2025)*
     - Taxonomy of causal methods actually used (RCTs, quasi-experiments, causal graphs, causal discovery, counterfactual analysis, Granger causality, SEM, propensity scores, causal fault localization, regression-based causal inference, etc.)
     - Trend analysis: volume of empirical SE papers vs. papers asking causal RQs vs. papers employing causal methods — quantifying the gap between causal ambition and methodological rigor
     - Summary of findings: which methods dominate (RCTs and causal fault localization), which are underrepresented (quasi-/natural experiments, IV, DiD, RDD), and what this implies for the field
   - 2.4 Parallel causal inference challenges in psychology and health research (cross-disciplinary context: the causal language taboo, the gap between causal ambition and methodology, reform efforts and lessons for SE)
   - 2.5 The PL vs. defect proneness debate (comprehensive review of all related work)

3. **A Primer on Causal Inference for SE Researchers** — Self-contained, accessible introduction:
   - 3.1 Why correlation does not imply causation (confounding, reverse causality, selection bias — illustrated with PL example)
   - 3.2 Why multivariate regression usually does not suffice (omitted variable bias, bad controls, when regression *can* support causal claims)
   - 3.3 The potential outcomes framework (notation, estimands, identification)
   - 3.4 Graphical causal models and DAGs (back-door criterion, connecting DAGs to potential outcomes)
   - 3.5 Overview of identification methods (RCTs, DiD, IV, RDD, panel FE, synthetic control) with assumptions and estimands
   - 3.6 The internal–external validity trade-off and the hierarchy of evidence

4. **The Four-Step Causal Credibility Assessment Framework**
   - 4.1 Step 1: Derive an explicit causal theory from domain knowledge
   - 4.2 Step 2: Define the causal estimate of interest and specify the identifying assumption
   - 4.3 Step 3: Honestly acknowledge and mitigate limitations and known caveats
   - 4.4 Step 4: Thoughtfully navigate alternative explanations

5. **Worked Example: The Programming Language and Defect Proneness Debate**
   - 5.1 Applying the four steps to Ray et al. (2014) and subsequent work
   - 5.2 Downstream causal misinterpretation analysis (citation analysis showing correlational findings reinterpreted as causal)
   - 5.3 Assessment summary: ambiguous interpretation, limited identification, unproductive debate

6. **From Assessment to Improved Design: A Panel Fixed Effects Analysis**
   - 6.1 Research design (exploiting within-developer and within-repository variation)
   - 6.2 Data construction
   - 6.3 Results and interpretation
   - 6.4 Limitations and remaining threats

7. **Discussion** — Implications for SE research practices, when and how to apply the framework, relationship to other methodological reform efforts (pre-registration, registered reports, replication)

8. **Conclusion**

## Literature Review Plan

Four systematic literature review efforts are needed to accurately frame the contribution and ensure comprehensive coverage. These reviews should be conducted before finalizing the paper framing and contribution statement.

### LR1: Existing Tutorials and Methodological Guides in SE

**Goal:** Identify all existing tutorial papers, methodological primers, and guideline papers in SE venues that touch on causal inference, research methodology, statistical methods, or evidence-based SE. This is critical for positioning our contribution and demonstrating the gap our paper fills.

**Search strategy:**
- Venues to search: ICSE, FSE/ESEC-FSE, ASE, MSR, EMSE, TSE, TOSEM, IST, JSS, and key methodological venues (e.g., EASE, ESEM)
- Search terms: "tutorial" OR "primer" OR "guidelines" OR "causal inference" OR "causal" OR "quasi-experiment" OR "research methodology" in SE venues
- Also search for methodological papers by known advocates of empirical rigor in SE (e.g., work by Shull, Singer, Basili, Kitchenham, Wohlin, Stol & Fitzgerald, Ralph, etc.)

**Key questions to answer:**
1. Are there any existing tutorials specifically on causal inference for SE? If so, what do they cover and what gaps remain?
2. What tutorials exist on adjacent topics (e.g., controlled experiments in SE, survey methodology, case studies, mining software repositories methodology)?
3. How do existing SE methodology papers treat causal claims — do they discuss identification strategies, or do they remain at the level of statistical testing?
4. What is the state of adoption of causal inference methods in empirical SE research? (Are there papers surveying this?)
5. Are there tutorial papers from adjacent fields (e.g., HCI, information systems, management) that we should reference as models?

**Existing analysis:** The notebook `notebooks/literature_review.Rmd` (reading from `data/se_papers_metadata.csv`) already contains a systematic classification of 100 SE papers from ASE, FSE, and ICSE (2015–2025) that engage with causality. Each paper is coded by `causal_type` (claim, method, or both) and, for papers using causal methods, by `causal_method_class` (a 13-category taxonomy). The notebook produces a bar chart of method prevalence and a trend plot of causal claims vs. causal methods over time. These results form the empirical backbone of Section 2.3.

**Expected deliverable:** A table mapping existing tutorials/guides by topic, venue, and the extent to which they address causal reasoning. A clear articulation of the gap our paper fills. The taxonomy and trend analysis from `literature_review.Rmd` should be refined and incorporated into Section 2.3 of the paper.

### LR2: Intellectual Traditions of Causal Inference and Causal Claim Assessment

**Goal:** Trace the historical development of causal inference from its origins through to the modern state of the art, ensuring comprehensive coverage of the different intellectual traditions and frameworks. The review should tell a concise story of how the field evolved---from early epidemiological reasoning through the formalization of experimental and counterfactual frameworks to the credibility revolution and its modern extensions---so that SE researchers can understand not just the current toolkit but how and why it came to be.

**Search strategy:**
- Historical foundations: Snow (1855, the origin of epidemiological causal reasoning), Neyman (1923, potential outcomes), Fisher (1935, randomized experiments), Hill (1965, observational causal assessment)
- Formalization of the counterfactual framework: Rubin (1974, potential outcomes for observational studies), Rosenbaum & Rubin (1983, propensity scores)
- The design-based tradition and credibility revolution: Card & Krueger (1994, landmark DiD), Angrist, Imbens & Rubin (1996, IV/LATE), Angrist & Pischke (2010, the credibility revolution manifesto)
- Graphical causal models: Pearl (2009, DAGs and do-calculus)
- Integrative treatments: Shadish, Cook & Campbell (2002), Morgan & Winship (2015), Imbens (2020, PO vs. DAG comparison)
- Textbooks and pedagogical references: Cunningham (2021), Hernán & Robins (2020), Huntington-Klein (2021), Hansen (2022)
- Recent methodological advances: DiD (Callaway & Sant'Anna 2021, Roth et al. 2023), double/debiased ML (Chernozhukov et al. 2018), causal forests (Athey & Imbens)
- Sensitivity analysis: Rosenbaum (2002), Oster (2019), Cinelli & Hazlett (2020)
- Debates within the causal inference community (e.g., Pearl vs. Rubin, DAGs vs. potential outcomes, structural vs. design-based)

**Key questions to answer:**
1. What are the major intellectual traditions and how do they relate to each other? Where do they agree and disagree?
2. Which traditions are most relevant and accessible for SE researchers? Which are currently underrepresented in SE?
3. How should we position the "four-step framework" relative to existing frameworks (e.g., Bradford Hill viewpoints, GRADE framework in medicine, the credibility revolution in economics)?
4. What sensitivity analysis methods exist and which are most applicable to SE settings?
5. Are there recent developments (e.g., ML-based causal inference methods) that we should cover, at least at a high level?

**Expected deliverable:** A structured overview of the landscape, a mapping of how our framework draws from each tradition, and a clear pedagogical path through the material that respects the nuances without overwhelming SE readers.

### LR3: The Programming Language vs. Defect Proneness Debate

**Goal:** Compile a comprehensive bibliography of all papers related to the question of whether programming language choice affects software quality / defect proneness. This includes the core debate papers, all papers citing them, independent studies on the topic, and related work on PL effects on other outcomes (productivity, security, maintainability).

**Core papers in the debate:**
- Ray et al., FSE 2014: "A Large Scale Study of Programming Languages and Code Quality in GitHub" (and the CACM 2017 extended version)
- Berger et al., TOPLAS 2019: "On the Impact of Programming Languages on Code Quality"
- Ray et al., arXiv 2019: rebuttal
- Berger et al., arXiv 2019: counter-rebuttal
- Furia et al., TOSEM 2024: structural causal model analysis of the PL-defect question

**Search strategy:**
- Forward citation search from the core papers (Google Scholar, Semantic Scholar)
- Search for papers on "programming language" AND ("defect" OR "bug" OR "fault" OR "quality" OR "reliability" OR "safety") in SE venues
- Search for papers using causal methods (DiD, IV, RDD, fixed effects, matching) in SE that study PL effects
- Search for the broader PL effectiveness literature (not just defects — also productivity, security, maintainability)
- Search for controlled experiments on PL effects, especially the Hanenberg research program on type systems (Hanenberg 2010; Mayer et al. 2012; Hanenberg et al. 2014 EMSE) and quasi-experimental studies (Nanz & Furia 2015 via Rosetta Code; Gao, Bird & Barr 2017 via type-checker bug detection on real JavaScript projects)

**Key questions to answer:**
1. What is the complete set of empirical studies examining PL effects on defect proneness or code quality?
2. How have downstream papers cited Ray et al. — correlationally or causally? (Extends the citation analysis from the thesis)
3. Have any studies used causal inference methods (beyond correlational regression) to study PL effects? If so, what did they find?
4. What do controlled experiments (e.g., developer studies) say about PL effects, and how do their findings compare with observational studies?
5. What does the PL research community (as opposed to the SE community) say about this question?
6. How does Furia et al. (2024) relate to our work, and how should we position ourselves relative to it?

**Expected deliverable:** A comprehensive annotated bibliography, a narrative synthesis of the state of the debate, and a clear articulation of what our worked example adds beyond what is already known.

### LR4: Revisiting Similar Problems in Psychology and Health Research

**Goal:** Document how psychology and health research have confronted the same causal inference gap that we identify in SE---the disconnect between causal ambition and methodological practice in observational research. This cross-disciplinary review strengthens the motivation for our tutorial by showing that the SE community's struggle is part of a broader pattern across empirical sciences, and that solutions emerging in adjacent fields can inform SE's methodological reform.

**Search strategy:**
- Key papers on the causal language problem in health research (Hernán 2018, Haber et al. 2022)
- Papers documenting the "taboo" against causal inference in psychology (Grosz, Rohrer & Thoemmes 2020)
- Methodological reform efforts introducing causal tools to psychology (Rohrer 2018, 2024; Wysocki et al. 2022)
- Estimand-first frameworks in social science (Lundberg, Johnson & Stewart 2021)
- Systematic reviews of causal methodology adoption in health research (Tennant et al. 2021 on DAG usage)
- Editorial guidance on causal inference reporting in clinical journals (Lederer et al. 2019)
- High-profile case studies where causal assumptions in observational research were contested (Killingsworth, Kahneman & Mellers 2023; Rohrer & Wenz 2024)

**Key questions to answer:**
1. How do psychology and health research parallel SE in their gap between causal ambition and methodological practice?
2. What institutional responses (editorial policies, reporting guidelines) have emerged in health research that SE venues have not yet adopted?
3. Which pedagogical models from psychology (e.g., Rohrer 2024) and epidemiology (e.g., Hernán's target trial framework) can inform our tutorial's approach?
4. What are the consequences of the causal language taboo across disciplines, and how does the SE community exhibit the same patterns?
5. How do high-profile observational debates in psychology (income-happiness) mirror the PL-defect debate in SE?

**Expected deliverable:** A cross-disciplinary narrative showing that SE's causal inference gap is systemic across observational empirical sciences, with specific lessons from psychology and health research that inform our four-step framework and motivate its adoption in SE.

## Task Backlog

### Phase 0: Literature Review and Framing (Current Phase)

- [x] **LR1a:** Classify causal methods in top-venue SE papers (ASE + FSE + ICSE, 2015–2025) — taxonomy and trend analysis implemented in `notebooks/literature_review.Rmd`; data in `data/se_papers_metadata.csv`
- [ ] **LR1b:** Complete literature review on existing SE tutorials and methodological guides (extend beyond top-3 venues to EMSE, TSE, TOSEM, IST, JSS, EASE, ESEM; identify tutorial papers specifically)
- [ ] **LR1c:** Refine taxonomy and trend analysis for paper-ready figures (polish labels, add confidence intervals to trends, compute inter-rater reliability if double-coded)
- [ ] **LR2:** Conduct literature review on intellectual traditions of causal inference
- [ ] **LR3:** Conduct literature review on the PL vs. defect proneness debate
- [ ] **LR4:** Conduct literature review on parallel causal inference problems in psychology and health research
- [ ] Synthesize findings from LR1–LR4 to finalize paper framing and contribution statement
- [ ] Revise paper structure based on literature review findings
- [ ] Write a 1-page "positioning statement" articulating the novelty relative to existing work (especially Furia et al. 2024)

### Phase 1: Tutorial Drafting

- [ ] Write Introduction (Section 1)
- [ ] Write Background & Related Work (Section 2), informed by LR1–LR4
- [ ] Write the Causal Inference Primer (Section 3), drawing from thesis Chapter 2 but adapted for a standalone tutorial format
- [ ] Write the Four-Step Framework (Section 4)
- [ ] Write the Worked Example (Section 5): apply four-step assessment to Ray et al. and the debate
- [ ] Conduct and write up the downstream citation analysis (Section 5.2)

### Phase 2: Empirical Study

- [ ] Construct panel dataset from GHArchive (identify polyglot developers and repositories)
- [ ] Operationalize language assignment at the commit level
- [ ] Compute defect metrics across multiple operationalizations
- [ ] Implement panel fixed effects analysis
- [ ] Assess within-developer variation and statistical power
- [ ] Conduct specification tests and robustness checks
- [ ] Write up findings (Section 6)

### Phase 3: Integration and Submission

- [ ] Write Discussion (Section 7)
- [ ] Write Conclusion (Section 8)
- [ ] Full paper revision and internal review
- [ ] Submit to TOSEM

## Key Risks and Open Questions

1. **Positioning relative to Furia et al. (2024):** They have already applied structural causal models to the PL-defect question. How do we differentiate? Our contribution is broader (a general tutorial framework, not just one application) and includes an empirical component (panel FE analysis), but we need to clearly articulate this.

2. **Scope management:** The tutorial could easily become a textbook chapter. We need to balance comprehensiveness with accessibility and stay within TOSEM page norms. The primer (Section 3) needs to be self-contained but not exhaustive.

3. **Empirical study feasibility:** The panel FE analysis depends on sufficient within-developer language variation in the data. If most developers are single-language, the estimator will lack power. Mitigation: assess variation early; fall back to within-repository variation or developer random effects if needed.

4. **Framing the contribution:** Is this primarily a tutorial paper (methodological contribution) or an empirical paper with a tutorial component? The framing affects the review criteria. For TOSEM, a tutorial/survey paper category may be most appropriate if available.

5. **Audience calibration:** The paper must be accessible to SE researchers with no causal inference background while also being rigorous enough to satisfy methodologists. This is a difficult balance to strike.

## References (Key)

- Ray, D., Posnett, D., Filkov, V., & Devanbu, P. (2014). A Large Scale Study of Programming Languages and Code Quality in GitHub. FSE 2014.
- Ray, D., Posnett, D., Filkov, V., & Devanbu, P. (2017). A Large-Scale Study of Programming Languages and Code Quality in GitHub. CACM 2017.
- Berger, E. D., Hollenbeck, C., Maj, P., Vitek, O., & Vitek, J. (2019). On the Impact of Programming Languages on Code Quality. TOPLAS 2019.
- Furia, C. A., Torchiano, M., & Tempero, E. (2024). Structural causal models analysis of PL and defects. TOSEM 2024.
- Pearl, J. (2009). Causality: Models, Reasoning, and Inference. Cambridge University Press.
- Rubin, D. B. (1974). Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies. Journal of Educational Psychology.
- Angrist, J. D., & Pischke, J.-S. (2009). Mostly Harmless Econometrics. Princeton University Press.
- Cunningham, S. (2021). Causal Inference: The Mixtape. Yale University Press.
- Hernán, M. A., & Robins, J. M. (2020). Causal Inference: What If. Chapman & Hall/CRC.
- Rosenbaum, P. R. (2002). Observational Studies. Springer.
- Hill, A. B. (1965). The Environment and Disease: Association or Causation? Proceedings of the Royal Society of Medicine.
