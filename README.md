# Causal Inference for Empirical Software Engineering: A Tutorial

**Target Venue:** ACM Transactions on Software Engineering and Methodology (TOSEM)

**Status:** Sections 1--3 drafted and revised; Section 4 (worked example) and Section 5 (discussion/conclusion) TODO. Appendices A--D drafted.

## Repository Organization

- `paper/`: LaTeX source code, compiled PDF, and bibliography for the manuscript.
- `notebooks/`: R Markdown notebooks for data analysis (literature review, cross-sectional and longitudinal analyses of the worked example, and prior reanalysis notebooks).
- `data/`: A Git submodule pointing to the [CausalityInSE-Data](https://github.com/hehao98/CausalityInSE-Data) repository, which stores large datasets (e.g., `commits.csv.zip`, `se_papers_metadata.csv`). This separation prevents large files from bloating the main repository.
- `plots/`: Generated figures used in the paper (e.g., `causal_trends.pdf`).
- `plans/`: Detailed sub-plans for specific tasks (see Plan Management Convention in `AGENTS.md`).
- `scripts/`: Utility scripts for data processing and analysis.
- `slides/`: Presentation slide decks related to this project.
- `thesis/`: Related thesis materials.

## Paper Vision

*"Correlation does not imply causation"* is among the most widely repeated methodological maxims in empirical software engineering --- technically correct, but not particularly useful. In practice, it appears in a limitations section, after which findings are left for readers to interpret as they see fit.

The practical questions motivating much empirical SE research are **causal in nature**: They concern the consequences of decisions, interventions, and changes to practice (e.g., does code review reduce defects? does AI-assisted development improve velocity?). This creates a productive tension: The questions we care about most are causal, yet the studies we can feasibly conduct are often observational. Despite the SE community's delicate dance pursuing causal inference from observational data, there is no consensus in the field, and the field lacks a shared vocabulary and toolkit to convey the strength of causal evidence in each study.

**Our vision:** The field needs to move forward and adopt the modern causal inference toolkit as the new standard for intervention-outcome questions involving observational SE data. Importantly, the power of the toolkit lies in making identifying assumptions **transparent and open to scrutiny**, ensuring that the strength of evidence is clearly communicated and that the field can iteratively develop stronger designs.

**The room for improvement is huge.** A classification of all main-track papers at ICSE, FSE, and ASE from 2015 to 2025 (5,341 papers) reveals that 40% are empirical SE studies, 29% of those ask or are motivated by a causal research question about interventions and outcomes, but only 1.9% of all papers claim to employ any recognized causal inference method. The ratio of causal motivation to causal method use has remained roughly 7-to-1 throughout the decade, indicating a structural gap rather than a transitional one. Among the papers that do use causal methods, randomized controlled experiments dominate (37 papers), followed by regression-based causal inference (14) and causal fault localization (13). The design-based methods central to the credibility revolution in economics --- difference-in-differences, instrumental variables, regression discontinuity --- are nearly absent.

To achieve this vision, the paper provides:
1. An education on the causal inference vocabulary and methods, covering the potential outcomes framework, graphical causal models, and design-based identification strategies.
2. A pragmatic guide for conducting credible causal inquiry in empirical SE.
3. A worked example on the impact of AI coding tools in open-source software, demonstrating the full arc from naive comparison through cross-sectional methods to design-based longitudinal identification.

## Paper Structure

1. **Introduction** (Section 1)
   - Opens with the "correlation does not imply causation" maxim as a framing device --- technically correct but not useful as typically deployed.
   - Highlights the productive tension: The questions we care about most are causal, yet the studies we can feasibly conduct are often observational.
   - Observational evidence has supported credible causal conclusions across many sciences; the field needs to adopt systematic frameworks for deriving, communicating, and scrutinizing the assumptions under which observational evidence can support a causal interpretation.
   - Notes that SE researchers typically come from CS/engineering backgrounds with training in building artifacts, not designing observational studies of human behavior.
   - States contributions: (1) causal inference education, (2) pragmatic guide, (3) worked example on AI coding tools in OSS.

2. **Background and Related Work** (Section 2)
   - **2.1 The Causal Inference Toolkit: Origins and Scope.** Three intellectual traditions: potential outcomes (Neyman/Rubin), the credibility revolution (Angrist/Card/Imbens, 2021 Nobel), and graphical causal models (Pearl's DAGs).
   - **2.2 Existing Tutorials and Methodological Guides in SE.** Positions relative to Wohlin et al.'s textbook, ACM SIGSOFT Empirical Standards, Siegmund et al., Robillard et al., and recent prescriptive tutorials (IV tutorial by Graf et al., matching tutorial by Nocera et al., Rohrer's psychology tutorial).
   - **2.3 Causal Inference Adoption in SE to Date.** Literature review of 5,341 ICSE/FSE/ASE papers (2015--2025): classification methodology, the causal ambition--methodology gap, 13-category taxonomy of causal methods used (Table 1), trend figure (Figure 1), and implications.

3. **A Primer on Causal Inference for SE Researchers** (Section 3)
   - **3.1 What Does It Mean Exactly for X to Cause Y?** Two complementary perspectives: *counterfactual dependence* (Rubin/Lewis --- defines the target) and the *target trial* (Hernan --- provides the research design template). Both illustrated with the AI coding tools running example.
   - **3.2 Why Cannot We Use Descriptive and Correlational Evidence?** Why naive comparison and kitchen-sink regression fail: four failure modes (unobserved confounders, collider bias, mediator bias, reverse causality) demonstrated with the AI coding tools example. Concludes that regression *can* support causal claims under specific conditions, but those conditions require the formal frameworks in Section 3.3.
   - **3.3 The Causal Inference Toolkit.** Three pillars:
     - *Potential outcomes framework* (Section 3.3.1): Formalizes estimands (ATE, ATT, LATE), derives identifying assumptions (randomization, conditional ignorability), discusses sensitivity analysis tools (Rosenbaum bounds, E-values, robustness values).
     - *Graphical causal models and DAGs* (Section 3.3.2): DAG construction, back-door criterion, confounders vs. mediators vs. colliders, limitations of DAGs. Pedagogical DAG for the AI tools--velocity question (Figure 2).
     - *Design-based identification* (Section 3.3.3): DiD, IV, RDD, Panel FE --- each with SE examples. Summary table of methods, estimands, and key identification assumptions (Table 2). Data features mapped to design-based strategies (Table 3).
   - **3.4 A Pragmatic Stance for SE Research.** Synthesized guide: build on prior research; use counterfactual reasoning to frame designs; use DAGs for mechanisms and covariate selection; use design-based identification when possible; iterate between question, assumptions, and design; engage with alternative explanations; when clean identification is unavailable, be transparent. Concludes with promises and perils of causal inference specific to SE research (panel data abundance, compound treatments, SUTVA violations, noisy proxies). References an empirical standard for causal inquiries (Appendix D).

4. **Worked Example: The Impact of AI Coding Tools in Open-Source Software** (Section 4) --- *TODO*

   **Setting:** ~1,000 popular GitHub repos across 10 programming languages; ~300 with AI config files (treatment) and ~600 without (control).

   **Research Question:** How does adopting AI coding tools systematically (as signaled by AI config files in the repository) affect the repository's development velocity, measured by monthly commits?

   - **4.1 Cross-Sectional Methods** --- *TODO*
     - Stage 1: Naive comparison and kitchen-sink regression (descriptive comparison table, baseline OLS).
     - Stage 2: Diagnose selection bias and temporal collapse (true temporal DAG vs. collapsed cross-sectional graph; classify covariates as structurally pre-treatment vs. temporally ambiguous; OLS comparison table; sensitivity analysis with Oster bounds and sensemakr).
     - Stage 3: Estimator convergence (OLS vs. PSM vs. IPW with pre-treatment covariates converge --- the estimator is not the bottleneck, the identifying assumption is).
     - Takeaway: Cross-sectional MSR data suffers from temporal collapse; only within-repo longitudinal variation can make progress.

   - **4.2 Longitudinal Methods** --- *TODO*
     - Before/after comparison (most naive: no trend adjustment, no control group).
     - Interrupted time series (ITS): models the pre-treatment trend explicitly, tests for level shift and slope change at adoption; still no control group, so contemporaneous shocks remain confounded. Motivates the need for a control group (Figure: ITS box plot).
     - Difference-in-differences (DiD): The design-based leap. Build intuition through (a) the classic 2×2 diagram and (b) the TWFE regression specification as exposition only (no results shown). Flag TWFE's known limitations under staggered treatment with heterogeneous effects (Goodman-Bacon 2021, de Chaisemartin & D'Haultfoeuille 2020).
     - Two complementary modern DiD estimators:
       1. Callaway & Sant'Anna (2021) DiD without covariates — the natural extension of the 2×2 idea to staggered adoption.
       2. Borusyak et al. (2024) imputation DiD with time-varying covariates — motivated by the question of whether conditioning on covariates can sharpen the estimate.
     - The comparison is pedagogically valuable: Borusyak's time-varying covariates are post-treatment mediators that attenuate the ATT (mediator bias); CS without covariates avoids this but relies on unconditional parallel trends. The two estimators also use different aggregation weights. Together they bracket a plausible range for the ATT.
     - Combined event study plot (Figure) with pre-trends assessment for both estimators (CS: simultaneous confidence bands; Borusyak: joint Wald test).
     - Robustness: trimmed control group (dropping inactive repos), PSM-matched panel.
     - Longitudinal takeaway: Compare all estimates (before/after, ITS, CS DiD, Borusyak DiD) and contrast with cross-sectional estimates to quantify selection bias.

5. **Discussion and Conclusion** (Section 5) --- *TODO*
   - For reviewers: If a clear intervention-outcome RQ is posed, stop accepting correlation analyses without an explicit discussion of the extent to which they may support a causal claim and the assumptions under which they do so.
   - For researchers: Clear directions and pointers for learning these methods.
   - Limitation: Raising empirical standards cannot prevent superficial adoption of methods (analogous to the grounded theory adoption problem in SE).

**Appendices:**
- **Appendix A:** A Case Study on Downstream Misinterpretation: Ray et al. (2014/2017) citation analysis showing 2:1 ratio of causal to hedged interpretations among papers engaging substantively with the PL--quality finding. --- *Drafted.*
- **Appendix B:** Historical Development of the Causal Inference Toolkit and Parallels with Psychology/Epidemiology Reforms. --- *Drafted.*
- **Appendix C:** Frequently Asked Questions (18 questions covering practical concerns from skeptical SE researchers). --- *Drafted.*
- **Appendix D:** An Empirical Standard for Causal Inquiries in SE (following ACM SIGSOFT Empirical Standards format). --- *Drafted.*

---

## References (Key)

- Angrist, J. D. & Pischke, J.-S. (2009). *Mostly Harmless Econometrics.* Princeton University Press.
- Angrist, J. D. & Pischke, J.-S. (2010). The Credibility Revolution in Empirical Economics. *JEP.*
- Cunningham, S. (2021). *Causal Inference: The Mixtape.* Yale University Press.
- Hernán, M. A. (2018). The C-Word: Scientific Euphemisms Do Not Improve Causal Inference From Observational Data. *AJPH.*
- Hernán, M. A. & Robins, J. M. (2020). *Causal Inference: What If.* Chapman & Hall/CRC.
- Huntington-Klein, N. (2021). *The Effect: An Introduction to Research Design and Causality.* Chapman & Hall/CRC.
- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference.* Cambridge University Press.
- Ray, B., Posnett, D., Filkov, V., & Devanbu, P. (2014). A Large Scale Study of Programming Languages and Code Quality in GitHub. *FSE 2014.*
- Rohrer, J. M. (2018). Thinking Clearly About Correlations and Causation. *Advances in Methods and Practices in Psychological Science.*
- Rohrer, J. M. et al. (2024). That's a lot to Process! Pitfalls of Popular Path Models. *Advances in Methods and Practices in Psychological Science.*
- Rubin, D. B. (1974). Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies. *Journal of Educational Psychology.*
