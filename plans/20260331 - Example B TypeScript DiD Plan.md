# Example B: Bogner & Merkel — Diagnostic Assessment and TypeScript DiD Plan

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
- [ ] 1a. Extract creation date and stars from `JavaScriptRepos.txt` and
  `TypeScriptRepos.txt`; merge with the characteristics CSVs to build a
  unified analysis frame with columns: `lang`, `ncloc`, `commits_count`,
  `stars`, `creation_year`, `framework`, plus the four quality metrics.
- [ ] 1b. Produce a **covariate balance table** (Table 1 analog) comparing JS
  vs. TS on: ncloc, commits_count, stars, creation_year, framework
  distribution. Use standardized mean differences (SMD) as the primary
  imbalance statistic.
- [ ] 1c. Produce distribution plots (box plots or violin plots) for ncloc,
  commits_count, and stars by language, using the paper's Linux Libertine
  theme and width = 8, height = 3.
- [ ] 1d. Fit OLS regressions predicting each of the four metrics from
  `lang` alone (Bogner replication) and from `lang + ncloc + commits_count +
  creation_year + stars` (adjusted). Report coefficients and 95% CIs.
  Show whether controlling for observables attenuates the gap.
- [ ] 1e. Write the diagnostic narrative for Section 4.4:
  target trial, DAG with confounders, estimand decomposition.

**Expected finding**: Large SMDs on project size (ncloc, commits) and age will
illustrate that JS and TS repos are not comparable on observables,
motivating propensity score matching.

---

### Stage 2 — Propensity Score Matching (NO new data needed)

**Goal**: Reconstruct a more balanced comparison by matching JS and TS repos
on observed covariates; show how the original gap shrinks.

**Tasks:**
- [ ] 2a. Estimate a logistic regression for `P(TS | covariates)` where
  covariates are: log(ncloc), log(commits_count), log(stars), creation_year,
  framework dummies. Assess model fit (C-statistic, calibration plot).
- [ ] 2b. Apply 1:1 nearest-neighbor matching without replacement, caliper
  0.2 SD of the log-odds. Report match quality: SMDs pre- and post-match,
  number of matched pairs.
- [ ] 2c. Estimate the ATT (average treatment effect on the treated) on the
  four quality metrics using the matched sample. Compare with unmatched
  estimates from Stage 1.
- [ ] 2d. Sensitivity analysis: vary caliper (0.1 SD, 0.3 SD) and matching
  ratio (1:2); report robustness of coefficient signs and magnitudes.
- [ ] 2e. Write the matching narrative for Section 4.4, framing it as a
  first correction that reduces but cannot eliminate bias (because it only
  controls for observables and does not handle selection on unobservables
  such as team engineering culture and management quality).

**Expected finding**: The code quality and understandability gaps shrink after
matching; the bug-fix ratio and resolution-time results may flip or become
non-significant, illustrating outcome sensitivity to confounder control.

---

### Stage 3 — Treatment Decomposition via `any` Type at Repo Level (NO new data needed)

**Goal**: Sharpen the treatment from "TypeScript vs. JavaScript" to "type
system adoption intensity" using the repo-level `any` density already in the
data; motivate the file-level analysis in Stage 4.

**Tasks:**
- [ ] 3a. Within the 305 TS repos, regress each quality metric on
  `any_type_count_ncloc` controlling for log(ncloc), log(commits_count),
  creation_year. Report coefficients and scatter plots with a lowess smoother.
- [ ] 3b. Split TS repos into low/medium/high `any` usage tertiles; compare
  their quality metrics to each other and to matched JS repos from Stage 2.
  This creates a three-level quasi-treatment gradient:
  JS (no type checking) → TS-high-any (nominal typing) → TS-low-any (strict
  typing). Show that the gap is concentrated at the strict-typing end.
- [ ] 3c. Write the treatment decomposition narrative: the key RQ should be
  "What is the effect of adopting strict static typing?" rather than "Does
  using TypeScript improve quality?" Explain why the repo-level `any` analysis
  is still susceptible to inter-repo selection (strict-typing repos may be
  better-staffed), and frame Stage 4 as the design that controls for this.

---

### Stage 4 — Within-Repo File-Level Fixed Effects (NEEDS NEW DATA)

**Goal**: Test the dose-response hypothesis ("the more strictly a codebase
uses the type system, the fewer bugs it accumulates") using within-repo
variation across files, thereby controlling for all repo-level confounders.

**Identification logic**: This is the same FE logic as Example A (Section 4.3),
applied one level down. Many repos contain both `.js` and `.ts` files
simultaneously, or contain `.ts` files with heterogeneous `any` density.
Within the same repo, team quality, testing culture, organizational maturity,
and management practices are held constant. Comparing typed vs. untyped files
(or high-`any` vs. low-`any` files) within the same repo isolates the effect
of type annotation depth from repo-level selection bias.

**Why this is stronger than the DiD/migration approach**:
TypeScript adoption is gradual and messy — many repos remain hybrid for years,
and "migration date" is inherently fuzzy. A file-level analysis avoids the
need to define a clean treatment date, requires no parallel trends assumption,
and is feasible with the existing 305 TS repos plus the multi-lingual repos
already in the JS sample.

#### 4a. Scope and Sampling

Two complementary subsamples:

**Subsample A — Multi-lingual repos (both .js and .ts files)**:
- From the existing 604 repos, identify those with non-trivial shares of both
  `.js` and `.ts` files (e.g., TypeScript fraction between 10% and 90% of
  source files). These repos have within-repo JS vs. TS variation.
- Expand by searching GitHub for repos with ≥100 stars where GitHub's
  detected languages include both JavaScript and TypeScript with ≥ 20% share
  each. Target 100–150 such repos.

**Subsample B — Pure TS repos (dose-response via `any`)**:
- Use the existing 305 TS repos. Within each repo, `.ts` files vary in `any`
  density, providing a continuous dose of type strictness.
- No additional repo-level data collection needed; only file-level parsing.

#### 4b. File-Level Data Extraction (NEEDS NEW DATA)

**New data needed**: For each file in each sampled repo, collect:

| Variable | How to collect | Effort |
|---|---|---|
| File language | file extension (`.js` / `.ts`) | Trivial (ls + extension) |
| Bug-fix commit rate | `git log --follow -- <file>` + keyword heuristic | Medium (git scripting) |
| File LOC | `wc -l` or `cloc` at HEAD | Low |
| File age (days) | date of first commit touching the file | Medium (git log parsing) |
| Number of contributors | count unique author emails per file | Medium (git log parsing) |
| `any` density per file | regex count of `: any`, `as any`, `<any>` in `.ts` files | Low |

**Bug-fix commit rate definition**: For each file, count the number of
bug-fix commits (commits whose message matches the Berger keyword heuristic)
that touch this file, divided by the total number of commits touching this
file. This is the file-level analog of the repo-level bug-fix commit ratio
already in the Bogner & Merkel data.

**Tasks:**
- [ ] 4b-1. For each sampled repo, run:
  ```
  git log --name-only --format="%H %s %ad" --date=short
  ```
  to get the full commit-file history. Apply keyword heuristic to flag
  bug-fix commits. Aggregate to file level: total commits, bug-fix commits,
  first commit date, unique author count.
- [ ] 4b-2. Record file language from extension. For `.ts` files, run a
  regex pass (`grep -cE ': any\b|as any\b|<any>'`) to count `any` usages;
  divide by file LOC to get `any` density.
- [ ] 4b-3. Filter out: auto-generated files (e.g., `*.d.ts`, files in
  `node_modules/`, `dist/`, `build/`), test files (files in `test/`,
  `spec/`, `__tests__/`), and files with fewer than 10 total commits
  (insufficient signal).
- [ ] 4b-4. Merge file-level data with repo-level characteristics from the
  existing CSVs to enable repo FE and repo-level controls.

#### 4c. Estimation Models

**Model 1 — JS vs. TS within multi-lingual repos** (Subsample A):

```
bug_rate_f = α_repo(f) + β · is_ts_f
           + γ₁ · log(LOC_f) + γ₂ · file_age_f + γ₃ · n_contrib_f + ε_f
```

`β` is the within-repo bug-fix rate difference between `.ts` and `.js` files,
controlling for file size, age, and number of contributors. Standard errors
clustered at the repo level.

**Model 2 — `any` dose-response within TS repos** (Subsample B):

```
bug_rate_f = α_repo(f) + β · any_density_f
           + γ₁ · log(LOC_f) + γ₂ · file_age_f + γ₃ · n_contrib_f + ε_f
```

`β` is the slope of the dose-response: within the same repo, how much does
a one-unit increase in `any` density change the bug-fix rate?

**Model 3 — Combined model** (pooling both subsamples):

Interact `is_ts` with `any_density` to test whether the JS vs. TS gap closes
as TS repos adopt more `any` (i.e., does TS with high `any` look like JS?).

**Tasks:**
- [ ] 4c-1. Implement Models 1–3 in R using `fixest::feols()` with
  `cluster = ~repo_name`. Report coefficients, 95% CIs, and within-R².
- [ ] 4c-2. Produce a binned scatter plot (binscatter) for Model 2:
  `any` density on x-axis, residualized bug-fix rate (after removing repo FE)
  on y-axis, with a linear fit and 95% CI band.
- [ ] 4c-3. Robustness checks:
  - Exclude the newest 20% of files in each repo (recently added files
    have fewer commits and noisier bug-fix rates).
  - Restrict to files with ≥ 20 total commits (high-signal files only).
  - Replace the continuous `any` density with a binary indicator
    (`any_free`: zero `any` usages vs. at least one).
  - Add framework × creation_year interaction dummies to control for
    time-varying community norms within frameworks.

#### 4d. Honest Engagement with Remaining Threats

Three threats require explicit discussion in Section 4.4:

1. **File-level selection**: developers may assign stable, well-understood
   modules to JS (or to strict TS) and experimental, complex features to TS
   (or to lenient TS with heavy `any`). Mitigations: (a) control for file age
   and LOC as proxies for complexity; (b) restrict to files added after the
   repo first introduced TypeScript (so the developer made an active choice,
   not a legacy default); (c) compare results with and without the age/LOC
   controls to assess sensitivity.

2. **Reverse causality**: developers may add strict typing to the most
   buggy modules first (to refactor and stabilize them), creating a spurious
   positive correlation between type strictness and prior bugs. Mitigation:
   focus on files typed from their first commit (not converted later).
   Flag this threat in the paper and discuss it as a direction for future
   causal designs.

3. **Spillovers (SUTVA)**: well-typed modules export typed interfaces that
   reduce errors in adjacent `.js` or lenient-`.ts` files. This understates
   the treatment effect on typed files and violates SUTVA. Mention as a
   limitation; note that it would bias `β` toward zero, so a positive finding
   is conservative.

**Tasks:**
- [ ] 4d-1. Sensitivity analysis for file-level selection: re-run Models 1–2
  restricting to files whose first commit postdates the repo's first `.ts`
  file (i.e., files that were typed from inception).
- [ ] 4d-2. Write up the limitations discussion for Section 4.4, covering
  all three threats and their mitigations.

---

## Data Collection Summary

| What | Data needed | Already collected? | Effort |
|---|---|---|---|
| Covariate imbalance (Stage 1) | repo creation date, stars, framework | Yes (TXT/CSV files) | Low |
| Propensity matching (Stage 2) | same as above | Yes | Low |
| `any` dose-response at repo level (Stage 3) | any-type_count_ncloc | Yes (TS repos) | Low |
| File-level language & LOC (Stage 4b) | file extensions, `wc -l` | No — clone repos | Low |
| File-level bug-fix rate (Stage 4b) | `git log --follow` per file | No — git scripting | Medium |
| File-level `any` density (Stage 4b) | regex on `.ts` files | No — text parsing | Low |
| Expanded multi-lingual repos (Stage 4a) | GitHub API search | No — API query | Medium |

**Not needed** (compared to the original DiD plan):
- Historical SonarQube runs at checkpoints (Very high effort — dropped)
- Time-series panel construction across 3–7 years per repo (High — dropped)
- Clean migration date identification (Medium — dropped)
- Parallel trends validation (Medium — dropped)

---

## Writing Plan for Section 4.4

Structure following the diagnostic → constructive rhythm established in
Section 4.3 (Example A):

1. **Diagnostic (~1.5 pages)**: Selection bias in Bogner & Merkel.
   - Covariate balance table showing JS vs. TS repos are not comparable on
     observables (size, age, stars).
   - DAG: organizational maturity → language choice AND quality practices.
   - Treatment decomposition: "TypeScript" is not one thing; `any` density
     shows within-TS heterogeneity. The relevant treatment is "type system
     adoption intensity," not "TS vs. JS."
   - Target trial framing: ideal experiment randomizes type system adoption
     across otherwise identical files within the same project.

2. **Matching correction (~0.5 pages)**: First step, controls observables only.
   - Show how matching on repo observables attenuates the raw gap.
   - Explain why matching alone is insufficient (selection on unobservables
     such as team engineering culture remains).

3. **Within-repo file-level FE redesign (~1.5 pages)**:
   - Explain the identification logic: the repo FE absorbs all repo-level
     confounders; only within-repo file-to-file variation identifies `β`.
     Analogy with Example A's developer and repo FEs.
   - Model 1 results (JS vs. TS within multi-lingual repos): coefficient plot.
   - Model 2 results (`any` dose-response within TS repos): binscatter figure.
   - Robustness checks summary.
   - Honest limitations: file-level selection, reverse causality, spillovers.

4. **Segue to Section 4.5**: How Example B differs from Example A — both use
   within-unit FE, but the unit shifts from developer/repo (Example A) to
   file within repo (Example B); the treatment shifts from "language of the
   commit" to "type annotation depth of the file."

---

## Open Questions

1. **Sample size**: A single large multi-lingual repo can contribute thousands
   of files. With 100–150 repos from Subsample A and 305 repos from
   Subsample B, the file-level sample could easily reach 50,000–500,000
   observations. Check that within-repo variation is sufficient (i.e., enough
   repos have both typed and untyped files, or wide `any` density variation).

2. **Vue repos**: `VueRepos.txt` contains 15,870 Vue repositories (JS-based).
   Vue single-file components mix `.vue`, `.js`, and potentially `.ts`.
   Could expand Subsample A's control pool but requires careful handling of
   `.vue` file format.

3. **Migration DiD as future extension**: The original DiD plan (JS→TS
   migration events, panel construction, staggered adoption estimator) remains
   a valid design. It answers a different — and arguably sharper — causal
   question: "What happens to a specific project's quality *over time* after
   it adopts TypeScript?" The file-level FE answers "within a project at a
   given time, do more-typed files have lower bug rates?" Both questions are
   legitimate; the file-level approach is more feasible for this paper.
   Flag the DiD as a natural next step in the Discussion section.
