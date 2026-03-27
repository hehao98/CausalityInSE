# Reanalysis Improvement and Example A Writing Plan

## Current State

The notebook (`notebooks/toplas19_reanalysis.Rmd`) produces 4 models with
zero-sum contrasts on the Berger et al. (2019) GitHub commits dataset:

| Model | Fixed Effects | N obs | Sig. languages (p<0.05) |
|-------|-------------|-------|--------------------------|
| M1: NBR (Berger replication) | None | 1,039 | 9: C, C++, Clojure(-), Haskell(-), JS, Obj-C, Php, Python, Ruby(-) |
| M2: NBR + Repo FE | Project | 552 | 2: C++, Objective-C |
| M3: Poisson + Dev FE | Author | 13,370 | 5: C, C++, Haskell(-), Java, Javascript |
| M4: Poisson + Two-way FE | Author + Project | 21,185 | 2: C, Haskell(-) |

**Key finding**: Progressive FE reduces significant associations from 9 to 2.
Unobserved project- and developer-level heterogeneity drives most of the
original signal.

**Concerning observations**:
- M2 drops 487/1,039 observations as singletons (47% loss)
- M3 drops 41,204/55,128 observations (75% loss)
- M4 drops ~39,879/61,722 observations (65% loss)
- Results may be driven by the non-representative subsample that has
  within-unit variation

---

## Strategic Questions

### 1. Bootstrapping (Berger et al. Concern)

Berger et al. used weighted cluster bootstrap and reduced significant
languages from 11 to 4. Our M1 already uses cluster-robust SEs (the
analytical equivalent), roughly replicating their finding.

**Should we bootstrap our FE models (M2--M4)?**

Yes, but frame correctly:
- If bootstrap kills remaining significance -- this *strengthens* the
  tutorial's message. The point is not to prove "C causes bugs" but to show
  that identification strategy matters.
- If bootstrap preserves some -- shows FE-robust results survive additional
  inference adjustments.
- Either way, this is a pedagogical demonstration, not a standalone empirical
  contribution. The paper should explicitly disclaim that the FE analysis
  illustrates causal reasoning, not that it establishes the "true" language
  effect.

### 2. Overlap with Furia et al.

|  | Furia et al. (2022) | Furia et al. (2024) | Our analysis |
|--|---------------------|---------------------|--------------|
| **Data** | Same GitHub (Ray) | Rosetta Code | Same GitHub (Ray) |
| **Method** | Bayesian estimation | SCM / do-calculus | Panel fixed effects |
| **ID strategy** | None (better inference) | Model-based (DAG) | Design-based (within-unit) |
| **Contribution** | Better statistics | First causal ID in PL lit | Pedagogical demo |

**Key differentiators**:
1. Same data, different approach: We stay on GitHub data (unlike Furia 2024
   who switched to competitions) making comparisons with Ray/Berger direct.
   We change the identification strategy (unlike Furia 2022 who improved
   inference while keeping the same cross-sectional design).
2. Design-based vs. model-based: FE exploits within-unit variation
   (design-based path from Section 3.4), while Furia (2024) uses DAG-based
   covariate adjustment. These are complementary strategies from the toolkit.
3. Tutorial purpose: We don't claim to settle the debate. The analysis shows
   how the *same question on the same data* yields different conclusions
   under different identification strategies.

**Address in paper**: Section 4.3 should include a paragraph positioning the
analysis relative to both Furia papers. Acknowledge Furia (2024) as the first
causal ID in the literature, then explain why we take a different route.

### 3. Singleton/Sample Attrition

Potentially the most serious methodological issue:
- M2 loses 47% of observations (repos using only one language)
- M3 loses 75% (developers committing in only one language)
- Remaining observations are systematically different (polyglot repos/devs)

**How to address**:
- Report attrition explicitly and characterize the remaining sample
- Argue the FE subsample (multi-language units) is the *right* population
  for the question: "within the same developer/repo, does language predict
  bug rate?" requires within-unit variation by definition
- Acknowledge results don't generalize to monoglot repos/developers
- Compare distributions of key covariates between dropped and retained obs

---

## Phase 1: Strengthen the Notebook

- [ ] **1a.** Sample characterization: Compare dropped vs. retained
  observations for each FE model. Report language distributions, mean
  commits, mean bug rates.
- [ ] **1b.** Cluster bootstrap robustness check for M2--M4. Use
  `fwildclusterboot::boottest()` or manual cluster bootstrap. Report
  bootstrap CIs alongside cluster-robust SEs.
- [ ] **1c.** Berger-style weighted cluster bootstrap on M1 to directly
  compare with their Table 3 and verify the reduction from 11 to ~4.
- [ ] **1d.** LaTeX-formatted summary table suitable for inclusion in paper.
- [ ] **1e.** Evaluate time-period panels (yearly observations per
  repo-language or dev-language) to reduce singleton dropout and allow
  time FE. If beneficial, add as model M5.

## Phase 2: Write Section 4.3 (Example A)

Structure following the TODO skeleton in `paper/main.tex` (lines 767--780):

- [ ] **2a. Diagnostic (~1 page)**: Walk through the pragmatic stance on
  Ray et al.
  - *Target trial*: Ideal experiment = randomly assign languages. Shows why
    observational data is problematic (self-selection).
  - *DAG*: Developer skill, project complexity, org culture, ecosystem
    maturity all confound language choice AND defect rates.
  - *Estimand*: "Effect of language" conflates type system, paradigm,
    ecosystem, community norms. Ill-defined treatment.
  - *Design-based path*: Cross-sectional design precludes identification,
    but data has panel structure. FE absorbs time-invariant confounders.

- [ ] **2b. Constructive (~1 page)**: Panel FE approach and results.
  - Explain developer FE (controls for skill, habits) and repo FE (controls
    for maturity, complexity, testing culture).
  - Present progression: M1 -> M2 -> M3 -> M4 showing attenuation.
  - Key numbers: "Of 9 significant associations in the pooled model, only 2
    survive two-way fixed effects."
  - Include bootstrap robustness results.

- [ ] **2c. Limitations (~0.5 page)**: Honest engagement.
  - FE only absorbs *time-invariant* confounders. Time-varying confounders
    remain.
  - Singleton attrition: Results condition on multi-language units.
  - Compound treatment: "Language" remains a bundle of features.
  - SUTVA: Polyglot projects violate stable unit treatment value assumption.
  - Frame these as **motivating Example B** (TypeScript DiD with sharper
    treatment).

- [ ] **2d. Positioning paragraph**: Distinguish from Furia (2022) Bayesian
  and Furia (2024) SCM approaches.

## Phase 3: Remaining Paper Sections

- [ ] Section 4.4 (Example B: TypeScript DiD) -- separate effort
- [ ] Section 4.5 (Synthesis) -- after both examples done
- [ ] Section 5 (Discussion) and Section 6 (Conclusion)
- [ ] Revise abstract/intro TODOs with final empirical numbers
