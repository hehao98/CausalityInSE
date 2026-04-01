# Example B: Bogner & Merkel — Diagnostic Assessment, OVB Analysis, and Design Thinking

## Original Study Summary

Bogner & Merkel (MSR 2022, arXiv:2203.11115) compare 299 JavaScript and 305
TypeScript GitHub repositories (collected Jan 2012–Jun 2021, >16M lines of
code) on four quality metrics:

| Metric | JS mean | TS mean | TS better? |
|---|---|---|---|
| Code smells / ncloc | higher | lower | Yes |
| Cognitive complexity / ncloc | higher | lower | Yes |
| Bug-fix commit ratio | 0.126 | 0.206 | No (TS worse) |
| Avg bug resolution time (days) | 31.86 | 33.04 | No (TS slightly worse) |

Additional finding: within TS repos, `any` type density negatively correlates
with quality (Spearman ρ 0.17–0.26), suggesting type-system adoption depth
matters.

**Data on hand** (604 repos, cross-sectional snapshot):
- `JavaScriptMetrics.csv` / `TypeScriptMetrics.csv`: the four quality metrics
  per repo
- `JavaScriptReposCharacteristics.csv` / `TypeScriptReposCharacteristics.csv`:
  ncloc, code_smells, cognitive_complexity, framework, bug_issues_count,
  bug-fix_commits_count, commits_count, any-type_count (TS only)
- `JavaScriptRepos.txt` / `TypeScriptRepos.txt`: creation date, stars per repo
- `VueRepos.txt`: 15,870 Vue repos (creation date, stars) — unused by Bogner
  & Merkel but potentially useful as additional control universe

---

## Identification Problems in the Original Design

### Problem 1 — Selection Bias (Core Issue)

Projects *choose* their language; TypeScript adoption is not random.
TS projects tend to be:
- **Larger and more complex** (larger codebases benefit more from type
  checking), meaning they start from a different baseline on all four metrics.
- **Newer or later-stage** (TypeScript was released in 2012, popular from
  ~2017 onward), so TS repos often represent a more recent, more professional
  engineering culture.
- **Organizationally distinct** (many prominent TS repos are from companies
  with dedicated engineering teams: Microsoft, Google, Vercel, Grafana Labs),
  while the JS list skews more toward individual/community projects.

DAG: *team capability* and *organizational maturity* are common causes of both
(a) adopting TypeScript and (b) having lower code smells and better practices.
The raw JS vs. TS comparison conflates the language effect with these selection
differences.

### Problem 2 — Compound Treatment

"TypeScript vs. JavaScript" is not a single, clean treatment.
It bundles at minimum:
1. Static type checking at compile time
2. Mandatory type annotations as a form of documentation
3. TypeScript-specific tooling (richer IDE integration, refactoring)
4. Community and developer self-selection (TS attracts engineers who value
   type safety)

The relevant causal question is: **Does adopting a static type system improve
code quality for a given project and team?** The compound treatment blurs this.
The `any` type density metric partially operationalizes treatment intensity
(how much of the type system is actually used), but this is only available for
TS repos and is measured cross-sectionally.

### Problem 3 — No Confounder Adjustment

Bogner & Merkel report raw metric comparisons and Mann-Whitney tests.
No regression controls, no matching on observable characteristics.
This is equivalent to a naïve difference-in-means where all confounders are
ignored.

### Problem 4 — Static Snapshot Cannot Support Causal Claims

The data is a single-point cross-section as of June 2021.
Even if TypeScript projects look better today, this could reflect:
- (a) the language improving quality (the claimed effect),
- (b) higher-quality projects choosing TypeScript (selection), or
- (c) temporal confounding (newer, better-managed projects adopt TS and also
  happen to have lower defect rates for unrelated reasons).
Only a design that exploits temporal variation in language adoption can
separate (a) from (b) and (c).

---

## Progressive Improvement Plan

### Stage 1 — Diagnostic and Covariate Imbalance (NO new data needed)

**Goal**: Quantify the selection bias and show it is large enough to threaten
the original conclusions.

**Tasks:**
- [x] 1a. Extract creation date and stars from `JavaScriptRepos.txt` and
  `TypeScriptRepos.txt`; merge with the characteristics CSVs to build a
  unified analysis frame with columns: `lang`, `ncloc`, `commits_count`,
  `stars`, `creation_year`, `framework`, plus the four quality metrics.
- [x] 1b. Produce a **covariate balance table** comparing JS vs. TS on:
  ncloc, commits_count, stars, creation_year, framework distribution. Use
  standardized mean differences (SMD) as the primary imbalance statistic.
- [x] 1c. Produce distribution plots (violin plots) for ncloc, commits_count,
  and stars by language, plus a creation-year bar chart, using the paper's
  Linux Libertine theme and width = 8, height = 3.
- [ ] 1d. Write the diagnostic narrative for Section 4.4:
  target trial, DAG with confounders, estimand decomposition.

**Expected finding**: Large SMDs on project size (ncloc, commits) and age will
illustrate that JS and TS repos are not comparable on observables, motivating
the OVB analysis in Stage 2.

---

### Stage 2 — Cross-Sectional OLS and the OVB Problem (NO new data needed)

**Goal**: Show that OLS with observable controls attenuates the raw gap but
cannot resolve the bias; quantify how strong unobserved confounding would need
to be to explain the remaining effect using three complementary OVB methods.

**Key pedagogical point**: Propensity score matching shares the same
conditional ignorability assumption as OLS — both adjust only for observables.
Teaching both in a tutorial would be redundant and might give the false
impression that matching solves a problem OLS does not. OLS is simpler to
present and easier to extend with sensitivity analyses, so we use OLS as the
sole cross-sectional estimator and focus pedagogical effort on diagnosing
the limits of that approach.

**Tasks:**
- [x] 2a. Fit OLS regressions for each outcome: M0 (unadjusted) and M5
  (fully adjusted with log(ncloc), log(commits), log(stars), creation_year,
  framework). Report coefficient attenuation and HC3 robust SEs.
- [x] 2b. **Coefficient instability**: Fit a sequence of models adding
  controls one at a time (none → +log(nLOC) → +log(commits) → +log(stars) →
  +creation_year → +framework). Produce a coefficient trajectory plot showing
  how the TS coefficient changes at each step. If the coefficient is still
  moving when the last observable is added, the reader should worry about
  what happens with the unobserved ones.
- [x] 2c. **Cinelli & Hazlett (2020) sensitivity analysis**: Apply `sensemakr`
  to produce robustness values (the minimum partial R² that confounders would
  need with both treatment and outcome to explain away the effect) and
  benchmark them against observed covariates. Produce contour plots for the
  lead outcome.
- [x] 2d. **Oster (2019) proportional selection bounds**: Compute δ* (the
  ratio of selection on unobservables to selection on observables needed to
  drive the coefficient to zero) under R²_max = min(1, 1.3 × R²_long).
  Report for all four outcomes.
- [ ] 2e. Write the OVB narrative for Section 4.4, explaining that the three
  methods converge on the same conclusion: the remaining TS effect is fragile
  and plausibly explained by unobserved confounding.

**Expected finding**: The coefficient shrinks substantially with controls,
robustness values from sensemakr are low relative to observed covariate
benchmarks, and Oster δ* values are below or near 1, all indicating that
the causal claim is not robust to plausible omitted variable bias.

---

### Stage 3 — A Cleverer Design: Type System Adoption Intensity (NO new data needed)

**Goal**: Show that reframing the treatment — from "JS vs. TS" to "how
strictly the type system is used" measured by `any`-type density within TS
repos — improves the design on both the treatment definition and covariate
balance, but still cannot resolve all threats.

**Tasks:**
- [x] 3a. **Covariate balance within TS**: Split TS repos at the median of
  `any` density into "strict" (low any) and "lenient" (high any). Compute
  SMDs on ncloc, commits, stars, creation_year between the two groups.
  Compare with JS-vs-TS SMDs from Stage 1 to show the within-TS comparison
  is more balanced on observables.
- [x] 3b. **Dose-response OLS**: Within the 305 TS repos, regress each
  quality metric on `any_density` controlling for log(ncloc), log(commits),
  and creation_year. Report coefficients and scatter plots with linear fit.
- [ ] 3c. Write the design-thinking narrative: the `any` density design is a
  genuine improvement (sharper treatment, narrower comparison group, better
  observable balance) but remains cross-sectional and susceptible to
  repo-level selection on unobservables (rushed or legacy projects use more
  `any`). Motivate the need for longitudinal data.

**Expected finding**: SMDs within TS are smaller than across JS/TS. The
dose-response shows an association between `any` density and quality, but
the cross-sectional design cannot rule out reverse causality or confounding
by unobserved project characteristics.

---

### Stage 4 — Bridge to Longitudinal Panel Data (narrative only)

**Goal**: Articulate why cross-sectional data hits a ceiling and motivate
the next notebook.

This stage produces no new analysis. It is a concluding paragraph that:
1. Restates the fundamental reflection problem: cross-sectional data cannot
   distinguish "strict typing → quality" from "high-quality teams → strict
   typing."
2. Notes that even the cleverer `any` density design is susceptible to
   repo-level selection on unobservables.
3. Explains that what is needed is within-project temporal variation: observe
   the same project before and after it tightens its type discipline, or
   compare typed vs. untyped files within the same repo.
4. Points to the next notebook, which collects new longitudinal data and
   applies file-level fixed effects and/or difference-in-differences.

---

## Data Collection Summary

| What | Data needed | Already collected? | Effort |
|---|---|---|---|
| Covariate imbalance (Stage 1) | repo creation date, stars, framework | Yes (TXT/CSV files) | Low |
| OVB assessment (Stage 2) | same covariates as Stage 1 | Yes | Low |
| `any` dose-response within TS (Stage 3) | any-type_count_ncloc | Yes (TS repos) | Low |
| Longitudinal panel data (next notebook) | file-level commit histories | No — git scripting | Medium-High |

---

## Writing Plan for Section 4.4

Structure following the diagnostic → constructive rhythm established in
Section 4.3 (Example A):

1. **Diagnostic (~1.5 pages)**: Selection bias in Bogner & Merkel.
   - Covariate balance table showing JS vs. TS repos are not comparable on
     observables (size, age, stars).
   - DAG: organizational maturity → language choice AND quality practices.
   - Cross-sectional OLS with controls: coefficient attenuation shows
     observables explain part of the gap, but OVB assessment (coefficient
     instability, sensemakr, Oster bounds) shows the remaining effect is
     fragile.

2. **Design improvement (~1 page)**: Reframing the treatment.
   - Treatment decomposition: "TypeScript" bundles multiple interventions;
     `any` density isolates type system adoption intensity.
   - Within-TS dose-response: improved observable balance, suggestive
     association, but still cross-sectional.
   - Target trial framing: ideal experiment randomizes type strictness
     within the same project over time.

3. **Bridge to longitudinal design (~0.5 pages)**:
   - Articulate why cross-sectional data is inherently limited for this
     question: cannot separate treatment effect from selection.
   - Motivate file-level FE / DiD as designs that exploit within-project
     variation and control for time-invariant repo-level confounders.
   - Segue to the next section / notebook where new data is collected.

---

## Open Questions

1. **Which outcome to feature in the paper?** Code smells / nLOC and
   cognitive complexity / nLOC show the clearest TS-is-better pattern.
   Bug-fix ratio is the most counterintuitive (TS appears worse). The paper
   could lead with bug-fix ratio because the "surprising" finding is the
   best hook, then show how OVB assessment explains it.

2. **sensemakr contour plot**: Should the paper include the contour plot
   or just report robustness values in a table? The contour plot is visually
   compelling but may be unfamiliar to the SE audience.

3. **Scope of the longitudinal notebook**: File-level FE within the
   existing 604 repos, or expand to new repos with migration events?
   Need to decide scope for the paper.
