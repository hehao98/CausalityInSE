# Reanalysis Improvement and Example A Writing Plan

## Current State

The notebook (`notebooks/toplas19_reanalysis.Rmd`) produces 4 models with
zero-sum contrasts on the Berger et al. (2019) GitHub commits dataset:


| Model                        | Fixed Effects    | N obs  | Sig. languages (p<0.05)                                            |
| ---------------------------- | ---------------- | ------ | ------------------------------------------------------------------ |
| M1: NBR (Berger replication) | None             | 1,039  | 9: C, C++, Clojure(-), Haskell(-), JS, Obj-C, Php, Python, Ruby(-) |
| M2: NBR + Repo FE            | Project          | 552    | 2: C++, Objective-C                                                |
| M3: Poisson + Dev FE         | Author           | 13,370 | 5: C, C++, Haskell(-), Java, Javascript                            |
| M4: Poisson + Two-way FE     | Author + Project | 21,185 | 2: C, Haskell(-)                                                   |


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

### 1. Bootstrapping (Berger et al. Procedure)

#### What Berger et al. Actually Did

Berger et al.'s bootstrap (Section 4.2.4 of their paper) addresses
**outcome measurement error**, not cluster correlation. The keyword
heuristic used to label commits as "bug fixes" (searching for *error*,
*bug*, *fix*, *issue*, *mistake*, *incorrect*, *fault*, *defect*, *flaw*)
has a **36% false positive rate** and **11% false negative rate**, as
estimated by manual review with 10 independent developers (Section 4.1.4).

The bootstrap procedure has two components per iteration:
1. Resample projects (with their attributes) with replacement.
2. Regenerate the bug-fix count for each project *i* as a random variable:
   `bcommits_i* ~ Binom(bcommits_i, 1 - FP) + Binom(commits_i - bcommits_i, FN)`
   where FP = 0.36, FN = 0.11.
3. Refit the NBR on the resampled data.
4. Repeat 100,000 times. Apply Bonferroni: significant if 0.01/16th and
   (1-0.01)/16th quantiles of the coefficient histogram exclude 0.

This **shrinks point estimates toward zero** (Table 6e) and widens
uncertainty, reflecting the noise in `Y`. Cluster-robust SEs do *not*
replicate this --- they correct inference for correlated residuals within
clusters but leave point estimates unchanged and do not address outcome
mismeasurement. The earlier claim in this plan that "M1 already uses
cluster-robust SEs (the analytical equivalent)" was incorrect.

#### Do We Need This Bootstrap for Our FE Models (M2--M4)?

**Arguments against applying it:**

- **Overcorrection risk.** The 36% FP / 11% FN rates were estimated on the
  *original* Ray et al. dataset. Berger et al. applied data cleaning
  (deduplication, TypeScript removal, C/C++ header accounting) *before*
  bootstrapping, but the FP/FN rates were estimated on the *pre-cleaning*
  data. Our reanalysis uses the same pre-cleaning data, so the same rates
  nominally apply --- but we should note the rates may not generalize to
  the cleaned subset.
- **Uniform error assumption.** The bootstrap assumes FP and FN rates are
  uniform across languages and projects (Section 5.2 of Berger explicitly
  flags this as a limitation). In reality, error rates vary enormously:
  DesignPatternsPHP had 80% FP while tengine had 10%. If mislabeling
  correlates with language (e.g., languages whose communities use "fix" in
  non-bug commits), the bootstrap could over- or under-correct
  differentially across languages.
- **FE models already reduce the signal.** M4 (two-way FE) retains only 2
  significant languages from the original 9. Layering a bootstrap that
  independently shrinks estimates toward zero on top of FE attenuation may
  kill *all* remaining signal, making the demonstration uninformative ---
  we cannot distinguish "the effect is truly zero" from "we over-corrected."
- **Different identification target.** The FE models change the estimand
  (within-unit variation) and dramatically reduce the sample. The
  mislabeling rates from a cross-sectional sample may not apply to the
  within-unit residual variation that FE models exploit.

**Arguments for applying it:**

- **Intellectual honesty.** If we cite Berger's finding that the keyword
  heuristic is noisy, we should account for it rather than ignoring it.
- **Completeness.** Showing the full pipeline (FE + bootstrap) demonstrates
  how multiple corrections compound, which is pedagogically valuable.
- **Comparability.** Applying the same bootstrap to M1 lets us directly
  compare our Table with Berger's Table 6e, verifying our pipeline.

**Decision:** Apply the bootstrap to M1 (for direct Berger comparison) and
M4 (two-way FE, the strongest specification). This gives six results in
the final table: M1, M1+bootstrap, M2, M3, M4, M4+bootstrap. Showing the
bootstrap on both the weakest and strongest models demonstrates whether
outcome mislabeling changes conclusions at either end of the
identification spectrum. Use 1,000 iterations (sufficient for stable CIs
while keeping runtime practical). The paper should note the
uniform-error-rate limitation and acknowledge that a proper measurement
error correction for the FE setting would require language- and
project-specific FP/FN rates.

#### Implementation Plan

Apply the same bootstrap to M1 (`glm.nb`, no FE) and M4 (`fepois`,
author + project FE). Use 1,000 iterations with Bonferroni correction.
See the `toplas19_reanalysis.Rmd` notebook for the implementation.

**Key implementation notes:**
- Verify that the data contains `commits` (total commits) alongside
  `bcommits` (bug-fixing commits), which is needed for the FN term.
- For M4, resample at the project level (the coarser cluster), then
  refit `fepois` with two-way FE. Some resamples may fail to converge
  due to singleton issues --- wrap in `tryCatch` and skip failures.
- Compare M1 bootstrap results against Berger's Table 6, columns (a)
  and (e), to validate the pipeline before interpreting results.

### 2. Overlap with Furia et al.


|                  | Furia et al. (2022)     | Furia et al. (2024)       | Our analysis               |
| ---------------- | ----------------------- | ------------------------- | -------------------------- |
| **Data**         | Same GitHub (Ray)       | Rosetta Code              | Same GitHub (Ray)          |
| **Method**       | Bayesian estimation     | SCM / do-calculus         | Panel fixed effects        |
| **ID strategy**  | None (better inference) | Model-based (DAG)         | Design-based (within-unit) |
| **Contribution** | Better statistics       | First causal ID in PL lit | Pedagogical demo           |


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

- **1a.** Sample characterization: Compare dropped vs. retained
observations for each FE model. Report language distributions, mean
commits, mean bug rates.
- **1b.** Berger-style outcome-mislabeling bootstrap on M1 (FP=0.36,
FN=0.11, 1K iterations, Bonferroni correction). Compare directly
against Berger's Table 6, columns (a) and (e), to validate the pipeline
and verify the reduction from 11 to ~4 significant languages.
- **1c.** Same bootstrap on M4 (two-way FE) to test whether outcome
mislabeling changes conclusions under the strongest identification
strategy. This gives six total results: M1, M1+boot, M2, M3, M4,
M4+boot.
- **1d.** LaTeX-formatted summary table suitable for inclusion in paper.
- **1e.** Evaluate time-period panels (yearly observations per
repo-language or dev-language) to reduce singleton dropout and allow
time FE. If beneficial, add as model M5.

## Phase 2: Write Section 4.3 (Example A)

Structure following the TODO skeleton in `paper/main.tex` (lines 767--780):

- **2a. Diagnostic (~1 page)**: Walk through the pragmatic stance on
Ray et al.
  - *Target trial*: Ideal experiment = randomly assign languages. Shows why
  observational data is problematic (self-selection).
  - *DAG*: Developer skill, project complexity, org culture, ecosystem
  maturity all confound language choice AND defect rates.
  - *Estimand*: "Effect of language" conflates type system, paradigm,
  ecosystem, community norms. Ill-defined treatment.
  - *Design-based path*: Cross-sectional design precludes identification,
  but data has panel structure. FE absorbs time-invariant confounders.
- **2b. Constructive (~1 page)**: Panel FE approach and results.
  - Explain developer FE (controls for skill, habits) and repo FE (controls
  for maturity, complexity, testing culture).
  - Present progression: M1 -> M2 -> M3 -> M4 showing attenuation.
  - Key numbers: "Of 9 significant associations in the pooled model, only 2
  survive two-way fixed effects."
  - Include Berger-style bootstrap on both M1 and M4; discuss how outcome
  mislabeling interacts with different identification strategies.
- **2c. Limitations (~0.5 page)**: Honest engagement.
  - FE only absorbs *time-invariant* confounders. Time-varying confounders
  remain.
  - Singleton attrition: Results condition on multi-language units.
  - Compound treatment: "Language" remains a bundle of features.
  - SUTVA: Polyglot projects violate stable unit treatment value assumption.
  - Frame these as **motivating Example B** (TypeScript DiD with sharper
  treatment).
- **2d. Positioning paragraph**: Distinguish from Furia (2022) Bayesian
and Furia (2024) SCM approaches.

## Phase 3: Remaining Paper Sections

- Section 4.4 (Example B: TypeScript DiD) -- separate effort
- Section 4.5 (Synthesis) -- after both examples done
- Section 5 (Discussion) and Section 6 (Conclusion)
- Revise abstract/intro TODOs with final empirical numbers

