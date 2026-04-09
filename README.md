# Causal Inference for Empirical Software Engineering: A Tutorial

**Target Venue:** ACM Transactions on Software Engineering and Methodology (TOSEM)

**Status:** Drafting phase --- Sections 1--3 drafted; revising structure to align with updated paper story.

## Repository Organization

- `paper/`: Contains the LaTeX source code and compiled PDF of the manuscript.
- `notebooks/`: Contains R Markdown notebooks used for data analysis (e.g., `literature_review.Rmd`).
- `data/`: A Git submodule pointing to the [CausalityInSE-Data](https://github.com/hehao98/CausalityInSE-Data) repository, which stores large datasets (e.g., `commits.csv.zip`, `se_papers_metadata.csv`).
  This separation prevents large files from bloating the main repository and causing issues with tools like Overleaf.

## Paper Vision

Empirical SE encompasses a diverse set of problems. Among them, **intervention-outcome problems** --- does adopting practice X improve outcome Y? --- are particularly important because they have immediate implications for practice.

**Experiments** are the gold standard for such problems, but they have important limitations. For some problems, they cannot overcome the lack of external validity; for others, experiments are simply infeasible. The alternative is **observational data**, such as data from software repositories. Over the past two decades, the SE community has been engaged in a delicate dance pursuing causal inference from observational data. It is extremely challenging. Arguably, there is no consensus in this field, but one popular approach is to rigorously frame the study as presenting only descriptive and correlational evidence --- which is only *suggestive* of the causal ambition that motivates it.

However, this conservative approach --- and the lack of an explicit vocabulary and toolkit to convey the strength of causal evidence --- has important consequences:

1. **Downstream causal misinterpretation remains prevalent despite cautious framing.** The Ray et al. paper and the subsequent controversy are a classic example: appropriately hedged associational findings were widely reinterpreted as causal claims in downstream papers, tech media, and practitioner discourse.
2. **Even when some researchers use "causal inference" methods, others may not understand the specific aspect in which "causal inference" is better.** The field lacks a shared vocabulary for communicating the strength of evidence.

This state of affairs is unsurprising, as most empirical SE researchers do not enter the field with the training necessary to apply the modern causal inference toolkit (such training is typically taught in statistics, economics, and public policy programs, not CS).

**Our vision:** The entire empirical SE field needs to move forward by adopting the modern causal inference toolkit as the new standard for all causal inquiries involving observational software engineering data. Importantly, the power of this toolkit lies in making the identifying assumptions **transparent and open to scrutiny**. This transparent disclosure ensures that (1) the strength of causal evidence is clearly communicated to an audience unfamiliar with related methods, and (2) the field can iteratively develop the research question, data, and methods with less demanding assumptions and touch more critical problems (causal structures).

**The room for improvement is huge.** A review of the past 10 years of ICSE/FSE/ASE papers reveals that 29% have a causal ambition, but only 4% use a causal inference method. The 4% is predominantly experiments and causal fault localization --- many other methods are almost nonexistent.

To achieve this vision, the paper provides:
- An education on the causal inference vocabulary and methods,
- A pragmatic guide on how to do causal inference in empirical SE,
- A worked example throughout to illustrate, so researchers can embrace this.

The paper should be self-contained and pedagogically oriented so that an SE researcher with no prior exposure to causal inference can (a) understand the state of the art, (b) critically evaluate causal claims in existing work, and (c) apply the pragmatic stance to their own research.

## Paper Structure

1. **Introduction** (Section 1)
   - Opens with the diversity of empirical SE problems, highlighting intervention-outcome problems as particularly important for practice.
   - Experiments are the gold standard but have limitations: lack of external validity for some problems, infeasibility for others.
   - The alternative is observational data. The SE community's dominant approach --- presenting only correlational evidence suggestive of causal ambitions --- has two consequences: (1) downstream causal misinterpretation persists despite cautious framing (Ray et al. controversy as a classic example), and (2) the field lacks a shared vocabulary to communicate the strength of causal evidence.
   - This is unsurprising --- empirical SE researchers typically lack training in the modern causal inference toolkit (taught in stats, econ, public policy, not CS).
   - The vision: adopt the modern causal inference toolkit as the standard for causal inquiries with observational SE data. Its power lies in transparent, scrutinizable identifying assumptions.
   - Documents the adoption gap: 29% of empirical SE papers ask causal questions, yet only 4% use any causal method (predominantly experiments and causal fault localization).
   - States contributions: (1) an education on causal inference vocabulary and methods, (2) a pragmatic guide for empirical SE, (3) a worked example on the impact of AI coding tools in OSS.

2. **Background and Related Work** (Section 2)
   - Coverage of existing tutorials and methodological guidelines in SE (positioning our contribution).
   - A brief coverage of the history of causal inference (potential outcomes, DAGs, credibility revolution).
   - A review of recent SE studies with a causal ambition and a causal inference method (empirical analysis of ICSE/FSE/ASE papers, taxonomy and trend figures).
   - **Why is this hard for SE studies?** SE-specific challenges: unmeasured confounders (skill, culture), compound treatments, SUTVA violations, noisy outcome proxies, inherent panel data structure.
   - **A case study on Ray et al. on downstream misinterpretation:** Quantitative citation analysis documenting how appropriately hedged associational findings are reinterpreted as causal claims --- illustrating a systemic field-level pattern. Connects to Hernán (2018) causal language problem and the methodological reform literature.

3. **The Tutorial** (Section 3) --- Taught in mix with the worked example throughout.

   The tutorial uses a single running worked example --- **The Impact of AI Coding Tools in OSS** --- to make every concept concrete as it is introduced.

   - **3.1 What does it mean for X to cause Y?**
     - Four perspectives on causation: regular association, counterfactual dependence, interventionism, target trial.
     - Each illustrated with the AI coding tools example.

   - **3.2 Why can't we use descriptive and correlational evidence (i.e., a kitchen-sink regression)?**
     - Five failure modes: selection bias, unobserved confounders, collider bias, mediator bias, and reverse causality.
     - Demonstrated concretely through the worked example.

   - **3.3 How to articulate identification assumptions for a causal interpretation and relax them to be less demanding and more plausible?**
     - Potential outcomes (define *what* to estimate).
     - DAGs (encode *what* to assume).
     - Design-based identification (make assumptions *credible*).

   - **3.4 How do we use them in practice?**
     - Build on prior research and practitioner knowledge.
     - Use counterfactual reasoning to frame research designs.
     - Use DAGs to reason about mechanisms and covariate selection.
     - Use design-based identification when the setting permits.
     - Iterate between question, assumptions, and design.
     - Engage with alternative explanations.
     - When clean identification is unavailable, acknowledge honestly with known limitations.

4. **The Worked Example: The Impact of AI Coding Tools in OSS** (Section 4)

   **Setting:** 1,000 popular GitHub repos across 10 programming languages. ~300 repos with AI config files (treatment) and ~600 repos without (control).

   **Research Question:** How does adopting AI systematically (as signaled by AI config files in the repo) affect the repository's productivity?

   **Outcome:** Monthly commits as a measure of productivity.

   **TODO:** Construct the data to have a collider and a mediator, and possibly two-period data.

   - **4.1 Cross-Sectional Methods**
     - **Methods applied:**
       - Naive comparison between treated and control repos.
       - Use DAG to justify OLS covariate selection and compare with a kitchen-sink regression.
       - Compare kitchen-sink regression vs. DAG-justified regression in terms of robustness.
       - Compare DAG-justified OLS vs. PSM vs. IPW.
     - **Findings:**
       - 15x raw productivity difference between the two groups --- extremely strong selection bias.
       - DAG is informative, but in a cross-sectional setting many metrics become mediators due to future leakage (e.g., # stars, # PRs, # issues).
       - Nothing is robust because of plausible, strong unmeasured confounders (e.g., team member skill level).
       - OLS, PSM, and IPW yield the same result. **Using PSM or IPW does not automatically make a study "causal inference"!**
     - **Takeaway:** Cross-sectional analysis provides informative but less convincing evidence for causal inquiries. Need strong assumptions to support a causal claim, and the assumptions are hard to defend. A longitudinal setting with design-based identification can address unobserved confounders through before/after within-comparisons and provide cleaner tests of temporal dependence.

   - **4.2 Longitudinal Methods**
     - **Methods applied:**
       - Basic before/after comparison.
       - TWFE without time-varying covariates.
       - TWFE with time-varying covariates.
       - Modern DiD estimators.
     - **Findings:** TODO
     - **Takeaway:** TODO

5. **Discussion and Conclusion** (Section 5)
   - **For reviewers:** If a clear intervention-outcome RQ is posed, we should stop accepting correlation analyses without an explicit discussion of the extent to which they may support a causal claim and the assumptions under which they do so.
   - **For researchers:** Clear directions and pointers for learning these methods. It is much more accessible nowadays for researchers with a CS background, with all the advances in AI and agents.
   - **Important limitation:** Even if we raise the empirical standard, we cannot prevent people from pretending to use better methods (analogous to the grounded theory adoption problem in SE).

**Appendices:**
- Historical development of causal inference and parallels with psychology/epidemiology --- *Drafted.*
- Frequently Asked Questions --- *Drafted.*
- An Empirical Standard for Causal Inquiry in SE --- *Drafted.*

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

### Phase 2: Restructure and Revise Existing Sections

- [ ] Revise Introduction (Section 1) to reflect updated paper story: general intervention-outcome framing, experiments' limitations, observational data challenges, downstream misinterpretation, vision of transparent assumptions
- [ ] Revise Background and Related Work (Section 2):
  - [ ] Retain existing tutorials/guidelines coverage and causal inference history
  - [ ] Add subsection: why is causal inference hard for SE studies?
  - [ ] Move and expand the Ray et al. misinterpretation case study into Section 2 (previously Section 4.2)
  - [ ] Connect to Hernán (2018) causal language problem and methodological reform literature
- [ ] Revise the Tutorial (Section 3) to integrate worked example throughout:
  - [ ] Update 3.1 (four perspectives on causation) to use AI coding tools running example
  - [ ] Update 3.2 (failure modes) to demonstrate with the worked example
  - [ ] Update 3.3 (toolkit: potential outcomes, DAGs, design-based identification)
  - [ ] Update 3.4 (pragmatic stance) with worked example illustrations

### Phase 3: Worked Example --- The Impact of AI Coding Tools in OSS

- [ ] Construct the dataset: 1,000 popular GitHub repos across 10 languages; identify ~300 with AI config files and ~600 without; ensure data has a collider and a mediator; consider two-period structure
- [ ] Cross-sectional analysis (Section 4.1):
  - [ ] Naive comparison (document 15x raw difference)
  - [ ] DAG construction and DAG-justified OLS covariate selection
  - [ ] Kitchen-sink regression vs. DAG-justified regression robustness comparison
  - [ ] PSM and IPW estimation; demonstrate convergence with OLS
  - [ ] Write up cross-sectional findings and takeaway
- [ ] Longitudinal analysis (Section 4.2):
  - [ ] Basic before/after comparison
  - [ ] TWFE without time-varying covariates
  - [ ] TWFE with time-varying covariates
  - [ ] Modern DiD estimators
  - [ ] Write up longitudinal findings and takeaway

### Phase 4: Integration and Submission

- [ ] Write Discussion and Conclusion (Section 5):
  - [ ] Implications for reviewers (stop accepting correlational analyses without causal assumptions discussion)
  - [ ] Implications for researchers (accessible learning paths, AI/agent advances)
  - [ ] Limitation: raising empirical standards cannot prevent superficial adoption of methods
- [ ] Revise Introduction and Abstract to reflect final structure
- [ ] Full paper revision and internal review
- [ ] Submit to TOSEM

## Key Risks and Open Questions

1. **Dataset construction for the worked example:** Need to construct a compelling dataset of ~1,000 popular GitHub repos with AI config files as the treatment signal. The data must be designed to naturally exhibit a collider and a mediator for pedagogical purposes, and ideally support a two-period panel structure for the longitudinal analysis.

2. **Scope of the single worked example:** The new story threads one example throughout the entire tutorial. This provides pedagogical coherence but means the example must illustrate every concept (selection bias, collider bias, mediator bias, DAG reasoning, PSM/IPW, TWFE, DiD). The example needs to be rich enough to carry this load.

3. **Disposition of prior empirical work:** The Ray et al. panel FE analysis (Example A), Bogner & Merkel diagnostic (Example B), and Cursor ITS analysis (Example C) from previous notebooks are no longer the paper's main worked examples. The Ray et al. misinterpretation analysis moves to Section 2 as a case study. Decide whether to retain any prior analyses as supplementary material.

4. **Positioning relative to Furia et al. (2024):** They applied structural causal models to coding competition data. Our contribution differs: (a) we provide a general tutorial with a pragmatic stance, not just one application; (b) our worked example demonstrates a full progression from cross-sectional to longitudinal methods on real-world data.

5. **Audience calibration:** The paper must be accessible to SE researchers with no causal inference background while also being rigorous enough to satisfy methodologists. Threading the worked example throughout the tutorial should help with accessibility.

6. **Framing the contribution:** This is primarily a tutorial paper whose contribution is the education on causal inference methods, the pragmatic guide, and the worked example demonstrating the full progression. The paper addresses the **identification** dimension of empirical SE controversies and explicitly acknowledges that **measurement** (construct validity, noisy proxies, ambiguous treatments) is an equally important but orthogonal challenge.

## References (Key)

- Ray, D., Posnett, D., Filkov, V., & Devanbu, P. (2014). A Large Scale Study of Programming Languages and Code Quality in GitHub. FSE 2014.
- Ray, D., Posnett, D., Filkov, V., & Devanbu, P. (2017). A Large-Scale Study of Programming Languages and Code Quality in GitHub. CACM 2017.
- Berger, E. D., Hollenbeck, C., Maj, P., Vitek, O., & Vitek, J. (2019). On the Impact of Programming Languages on Code Quality. TOPLAS 2019.
- Furia, C. A., Torchiano, M., & Tempero, E. (2024). Structural causal models analysis of PL and defects. TOSEM 2024.
- Hernán, M. A. (2018). The C-Word: Scientific Euphemisms Do Not Improve Causal Inference From Observational Data. AJPH 2018.
- Pearl, J. (2009). Causality: Models, Reasoning, and Inference. Cambridge University Press.
- Rubin, D. B. (1974). Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies. Journal of Educational Psychology.
