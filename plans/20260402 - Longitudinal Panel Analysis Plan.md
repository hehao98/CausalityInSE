# Longitudinal Panel Analysis Plan

**Created:** 2026-04-02
**Purpose:** Analyze the monthly panel data (`data/ai_adoption_panel.csv`) as the natural follow-up to the cross-sectional diagnostic in `notebooks/ai_adoption_cross_sectional.Rmd`. The cross-section showed that the estimator is not the bottleneck --- unobserved confounding is. This notebook uses within-repo temporal variation to absorb time-invariant confounders and progressively builds toward a credible causal estimate.

---

## Data Summary

| Element | Value |
|---------|-------|
| **Repos** | 999 (balanced panel: every repo has 27 months) |
| **Time window** | 2024-01 through 2026-03 (27 months) |
| **Observations** | 26,973 repo-months |
| **Ever-treated** | 240 repos (staggered adoption, 2024-11 to 2026-03) |
| **Never-treated** | 759 repos (pure control group) |
| **Outcome** | `commits` (monthly commit count on default branch) |
| **Treatment** | `treated` (binary absorbing: 1 from first month with L2+ AI config file onward) |
| **Event time** | `months_since_treatment` (ranges from -27 to +16) |
| **Time-varying covariates** | `active_contributors`, `new_stars`, `new_issues`, `new_forks`, `new_releases` |
| **Time-invariant covariates** | `owner_type`, `queried_language`, `primary_language`, `created_at`, `license`, `ai_maturity_level` |
| **Collected but excluded from primary spec** | `prs_merged` (mechanistically downstream of commits --- conditioning blocks the causal path) |

---

## Pedagogical Arc

The notebook follows a **progression of increasingly credible designs**, each building on the previous one's limitations. This mirrors the tutorial's core message: identification is the bottleneck, and the design matters more than the estimator.

```
Cross-sectional estimate (from companion notebook)
  ↓ "Can't separate selection from effect"
Stage 0: Naive before/after (pre-post mean comparison)
  ↓ "Confounds treatment with secular trends"
Stage 1: Interrupted Time Series (single treated group, no controls)
  ↓ "No counterfactual --- what would have happened without treatment?"
Stage 2: TWFE DiD without time-varying covariates
  ↓ "Absorbs time-invariant confounders + common shocks, but
      time-varying confounders still threaten identification"
Stage 3: TWFE DiD with time-varying covariates
  ↓ "Addresses observable time-varying confounders, but TWFE is
      biased under staggered treatment with heterogeneous effects"
Stage 4: Borusyak et al. imputation DiD (modern estimator)
  ↓ "Solves staggered-treatment bias, uses covariates, yields
      clean event-study and ATT"
Summary comparison table
```

---

## Stage 0: Naive Before/After Comparison

**What it does:** For each ever-treated repo, compute mean monthly commits in the pre-treatment window (all months before `treatment_month`) vs. post-treatment window (treatment month onward). Report the average within-repo change.

**Implementation:**
- Restrict to the 240 ever-treated repos.
- For each repo, split observations into pre and post using `months_since_treatment`.
- Compute `mean_post - mean_pre` for each repo.
- Report the average change (and its distribution) across repos.
- Optionally report a paired t-test or signed-rank test.

**Key limitation:** No control group --- confounds the treatment effect with any secular trends (e.g., if repos tend to grow over time, the "effect" is partly trend).

---

## Stage 1: Interrupted Time Series (ITS) Without Controls

**What it does:** Model the outcome as a function of time, a level shift at treatment onset, and a slope change. This is the single-group version of ITS.

**Implementation:**
- Restrict to ever-treated repos (or run on the full panel with repo FE).
- Estimate: `log1p(commits) ~ time_trend + treated + months_since_treatment × treated + repo_FE`
  - `time_trend`: linear time trend (month index 1–27)
  - `treated`: level shift (does the intercept change at adoption?)
  - `months_since_treatment × treated`: slope change (does the trajectory change after adoption?)
- Cluster SEs at the repo level.
- Plot the average trajectory for treated repos with the fitted ITS line.

**Key limitation:** The counterfactual is the extrapolated pre-treatment trend for the *same group*. If something else changed at the same time as treatment (e.g., the repo went viral, or an external event affected all repos), the ITS confounds it with the treatment effect. There is no separate control group to benchmark against.

---

## Stage 2: TWFE DiD Without Time-Varying Covariates

**What it does:** The classic two-way fixed effects specification that absorbs all time-invariant repo heterogeneity and all common temporal shocks.

**Model:**
```
log1p(commits_it) = α_i + γ_t + β · treated_it + ε_it
```
- `α_i`: repo fixed effects (absorb language, org type, developer skill baseline, etc.)
- `γ_t`: month fixed effects (absorb seasonal patterns, platform-wide shocks)
- `β`: identified from within-repo, within-period variation in treatment status
- Cluster SEs at the repo level.

**Event study specification:**
```
log1p(commits_it) = α_i + γ_t + Σ_k β_k · 1{months_since_treatment_it = k} + ε_it
```
- Omit one reference period (e.g., k = -1) for identification.
- Trim event-time window to a reasonable range (e.g., k ∈ [-12, +12]) for readability.
- Pre-treatment coefficients (k < 0) test parallel trends.
- Post-treatment coefficients (k ≥ 0) show dynamic effects.

**Output:**
- [ ] TWFE coefficient table (ATT estimate, SE, p-value)
- [ ] Event study plot with 95% CIs
- [ ] Pre-trends F-test (joint test of all pre-treatment coefficients = 0)

**Key limitation:** No time-varying covariates --- if repo-specific shocks (e.g., going viral, losing a key contributor) coincide with treatment timing, the estimate is biased. Also, TWFE is biased under staggered treatment with heterogeneous treatment effects (already-treated units act as controls for later-treated units, and negative weights can arise).

---

## Stage 3: TWFE DiD With Time-Varying Covariates

**What it does:** Extends Stage 2 by adding time-varying controls that absorb repo-specific shocks.

**Model:**
```
log1p(commits_it) = α_i + γ_t + β · treated_it + δ · X_it + ε_it
```
- `X_it` includes: `log1p(active_contributors)`, `log1p(new_stars)`, `log1p(new_issues)`, `log1p(new_forks)`, `log1p(new_releases)`
- **Exclude** `prs_merged` from the primary specification: PRs are mechanistically downstream of commits (merging a PR is committing), so conditioning on them risks blocking the causal path.
- Cluster SEs at the repo level.

**Event study:** Same as Stage 2 but with `X_it` covariates included.

**Output:**
- [ ] TWFE coefficient table with and without covariates side by side
- [ ] Event study plot (with covariates)
- [ ] Compare ATT estimate with Stage 2 to assess how much time-varying confounders matter

**Key limitation:** Still inherits the TWFE bias under staggered treatment with heterogeneous effects. The time-varying covariates also carry a risk: if any of them are post-treatment (e.g., `new_stars` increases *because* of AI adoption), conditioning on them induces bias. The DAG should be reviewed: contributors and stars are plausibly contemporaneous confounders (they affect both adoption likelihood and commits), but if AI adoption causes more contributors or stars, they are mediators/colliders.

### Covariate DAG Review

For each time-varying covariate, assess whether it is a confounder (include) or a mediator (exclude):

| Covariate | Confounder story | Mediator story | Decision |
|-----------|-----------------|----------------|----------|
| `active_contributors` | More contributors → more commits AND more likely someone introduces AI tooling | AI adoption → attracts contributors | **Include with caution** --- primarily a confounder (contributor count in month t reflects team size that drives both treatment and outcome) |
| `new_stars` | Viral attention → more commits (new contributors) AND → AI adoption (new tech-savvy contributors bring AI config files) | AI adoption → hype/visibility → stars | **Include** --- the confounder story is stronger (stars reflect external attention shocks) |
| `new_issues` | User demand → more bug-fix commits AND → maintainer seeks AI tools for productivity | AI adoption → more responsive → more issues filed | **Include** --- primarily reflects external demand |
| `new_forks` | Community engagement shock → more commits AND → AI adoption | AI adoption → hype → forks | **Include** --- similar to stars |
| `new_releases` | Release cadence reflects organizational rhythm that drives both | AI adoption → faster releases | **Include with caution** --- could be downstream |

---

## Stage 4: Borusyak et al. Imputation DiD

**What it does:** The modern imputation-based DiD estimator from Borusyak, Jaravel, and Spiess (2024). This estimator:
1. Estimates the counterfactual outcome for treated (i, t) cells by fitting a model on untreated observations only (never-treated + not-yet-treated), then imputing what the treated units *would have done* absent treatment.
2. Treatment effects are the difference between observed and imputed outcomes for each treated (i, t) cell.
3. Naturally handles staggered adoption without the negative-weighting problem of TWFE.
4. Supports covariates (both time-varying and time-invariant, though the latter are absorbed by unit FE).

**R package:** `didimputation` (Butts & Gardner) or `did2s` --- check which implements Borusyak et al. most directly. The `didimputation` package by Kyle Butts implements the Borusyak et al. estimator via `did_imputation()`.

**Implementation:**

```r
library(didimputation)

# Full specification with time-varying covariates
did_imp <- did_imputation(
  data = panel,
  yname = "log_commits",
  gname = "treatment_cohort",    # first treated period (0 for never-treated)
  tname = "month_idx",           # numeric month index
  idname = "repo_id",            # numeric repo identifier
  first_stage = ~ log1p(active_contributors) + log1p(new_stars) +
                  log1p(new_issues) + log1p(new_forks) + log1p(new_releases),
  horizon = TRUE,                # event-study estimates
  pretrends = TRUE               # pre-trend coefficients
)
```

**Covariates to include:**

*Time-varying (in `first_stage` formula):*
- `log1p(active_contributors)`
- `log1p(new_stars)`
- `log1p(new_issues)`
- `log1p(new_forks)`
- `log1p(new_releases)`

*Time-invariant (absorbed by unit FE, but relevant for heterogeneity analysis):*
- `owner_type` (Organization vs. User)
- `queried_language`

**Output:**
- [ ] Average ATT estimate (the main number to compare with the cross-sectional coefficient)
- [ ] Event study plot with pre-treatment and post-treatment coefficients
- [ ] Pre-trends test
- [ ] Comparison with TWFE estimates from Stages 2–3 (do they diverge? if so, TWFE bias is present)

---

## Control Group Assessment: Do We Need Matching?

**The question:** The 759 never-treated repos serve as the control group. Are they comparable enough to the 240 ever-treated repos that the parallel trends assumption is plausible?

**Diagnostics to run:**

1. **Pre-treatment trajectory comparison:** Plot average monthly commits (or log commits) for ever-treated vs. never-treated repos in the pre-treatment window (before any repo adopts). If the trajectories are roughly parallel, the unmatched control group is adequate.

2. **Baseline covariate balance:** Compare time-invariant covariates (language, org type, repo age, baseline commit level) between ever-treated and never-treated repos. Report SMDs as in the cross-sectional notebook.

3. **If pre-trends fail or balance is poor:** Consider matching or trimming the control group:
   - Match on pre-treatment average commits (or growth rate) and key covariates using `MatchIt`.
   - Or restrict to repos within a common support region (e.g., drop repos with zero commits throughout the panel, as they are structurally different and will never adopt AI tools).
   - Re-run the DiD estimators on the matched/trimmed sample.

4. **Practical consideration:** With 759 controls and 240 treated, we have a 3:1 ratio --- ample for matching if needed. The key risk is that never-treated repos include many dormant/archived repos that have zero commits throughout the panel. These inflate the control group but do not contribute useful variation (they have flat trajectories that are trivially "parallel" but not informative).

**Decision criteria:**
- If the event study pre-treatment coefficients are close to zero and the pre-trends F-test is non-significant, the raw control group is adequate.
- If pre-trends fail, matching or trimming the control group becomes necessary before interpreting the ATT.

---

## Summary Comparison Table

The final output is a table comparing all estimates:

| Design | Estimate | 95% CI | Key assumption | Assumption plausible? |
|--------|----------|--------|----------------|----------------------|
| Cross-sectional OLS (M_pretreat) | from companion notebook | | Conditional ignorability (no unobserved confounders) | No --- massive covariate imbalance, unobserved developer skill |
| Cross-sectional OLS (M_extended) | from companion notebook | | Same + ambiguous covariates not mediators | No --- confounder vs. mediator ambiguity |
| Naive before/after | Stage 0 | | No secular trends | No --- commits trend over time |
| ITS (no controls) | Stage 1 | | Linear pre-treatment trend extrapolates | Weak --- no external counterfactual |
| TWFE DiD (no covariates) | Stage 2 | | Parallel trends + no time-varying confounders + homogeneous effects | Moderate --- event study tests pre-trends |
| TWFE DiD (with covariates) | Stage 3 | | Parallel trends conditional on X_it + homogeneous effects | Moderate-to-strong |
| Borusyak imputation DiD | Stage 4 | | Parallel trends conditional on X_it | Strong --- handles heterogeneous staggered effects |

---

## Implementation Checklist

### Notebook: `notebooks/ai_adoption_longitudinal.Rmd`

- [ ] **Setup:** Load packages (`fixest`, `didimputation`/`did2s`, `ggplot2`, `dplyr`, `showtext`, etc.)
- [ ] **Data prep:** Load `data/ai_adoption_panel.csv`, create `log_commits`, `month_idx`, `repo_id`, `treatment_cohort` (cohort = first treated month as integer, 0 for never-treated), log-transform time-varying covariates
- [ ] **Descriptive plots:**
  - [ ] Average monthly commits over time by treatment group (ever-treated vs. never-treated)
  - [ ] Staggered treatment timing histogram (how many repos adopt in each month)
  - [ ] Pre-treatment covariate balance between ever-treated and never-treated (SMD plot)
- [ ] **Stage 0:** Naive before/after comparison (treated repos only)
- [ ] **Stage 1:** ITS on treated repos (level + slope change, repo FE, no control group)
- [ ] **Stage 2:** TWFE DiD without covariates + event study plot + pre-trends F-test
- [ ] **Stage 3:** TWFE DiD with time-varying covariates + event study plot
- [ ] **Stage 4:** Borusyak imputation DiD with full covariates + event study plot + ATT
- [ ] **Control group assessment:** Pre-trends diagnostics, consider matching if needed
- [ ] **Summary table:** All estimates side by side with assumptions and plausibility

### Key R Packages

| Package | Purpose |
|---------|---------|
| `fixest` | Fast TWFE estimation with `feols()`, clustering, event studies via `i()` |
| `didimputation` | Borusyak et al. imputation estimator via `did_imputation()` |
| `ggplot2` + `showtext` | Plots with Linux Libertine font |
| `dplyr` / `tidyr` | Data wrangling |
| `MatchIt` | Control group matching (if needed) |
| `cobalt` | Balance diagnostics for matching |
| `modelsummary` or `kableExtra` | Coefficient tables |

### Plotting Conventions (from AGENTS.md)

- Font: Linux Libertine, base_size = 13
- Dimensions: `ggsave(width = 8, height = 3)` (or 8 × 4 for event study plots)
- Legend at bottom, minimal theme, no vertical grid lines
- Title Case for axis labels, sentence case for legend items

---

## Risks

1. **`didimputation` may not support `first_stage` covariates directly.** Check the package documentation. If not, consider `did2s` (Gardner 2022) which also implements imputation-based DiD with covariate support, or manually implement the two-stage procedure: (a) regress outcome on covariates + unit FE + time FE using only untreated observations, (b) impute counterfactuals for treated observations, (c) average the residuals.

2. **Pre-trends may fail.** This is informative, not a bug --- it would mean the parallel trends assumption does not hold even with covariates, and the DiD estimate is not credible. In that case, the finding is: "Even the longitudinal design cannot fully resolve the identification problem, because treated repos were already on different trajectories before adoption."

3. **Many zero-commit months.** The panel likely contains many (repo, month) cells with zero commits (dormant repos). `log1p(commits)` handles the zeros, but the distribution may still be highly skewed. Consider whether Poisson FE models (`fepois` in `fixest`) or negative binomial models are more appropriate for count outcomes. Report OLS on log1p as the primary specification for comparability with the cross-sectional analysis, and note the count-model robustness check.

4. **Treatment timing is concentrated in recent months.** Most adoptions happen in 2025–2026, so the post-treatment window for many repos is short (1–5 months). This limits statistical power for long-horizon dynamic effects and makes the event study sparse at large positive lags.
