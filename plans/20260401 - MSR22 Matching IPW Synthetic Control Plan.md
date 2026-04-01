# Plan: Matching, IPW, and Synthetic Control for MSR22 Reanalysis

## Context and Motivation

The current `notebooks/msr22_reanalysis.Rmd` implements a four-stage
progression on the Bogner & Merkel (MSR 2022) JS-vs-TS dataset (604 repos:
299 JS, 305 TS):

1. **Stage 1** — Replicate raw comparison; document covariate imbalance
   (SMDs: nLOC 0.06, commits 0.17, stars 0.40, creation year 0.75).
2. **Stage 2** — OLS with controls + three OVB diagnostics (coefficient
   instability, Cinelli & Hazlett sensemakr, Oster bounds). Conclusion:
   cross-sectional estimate is fragile (code smells RV = 8.9%, Oster
   δ* ≈ 1.15).
3. **Stage 3** — Within-TS dose-response on `any`-type density. Sharper
   treatment, better balance, but still cross-sectional.
4. **Stage 4** — Narrative bridge to longitudinal data.

The existing plan (`20260331 - Example B TypeScript DiD Plan.md`)
explicitly chose OLS over matching, arguing that they share the same
conditional ignorability assumption and that teaching both would be
redundant. This was pedagogically reasonable for a paper focused on
reaching longitudinal methods quickly, but it leaves a gap: the notebook
never demonstrates *how* matching, IPW, or synthetic control work in
practice, nor does it show whether these methods produce different answers
from OLS on this dataset.

This plan explores whether adding one or more of these methods would
strengthen the reanalysis as a pedagogical demonstration.

---

## Summary of Available Methods and Fit

### 1. Propensity Score Matching (PSM)

**What it does**: Pairs each TS repo with a similar JS repo (or vice versa)
based on estimated propensity to be TypeScript, using observable covariates.
Discards unmatched units; estimates ATT on the matched sample.

**What it adds beyond current OLS**:
- Makes the overlap (common support) problem visible — how many repos
  have no credible counterpart in the other language?
- Produces a **love plot** (SMD before vs. after matching) that is a
  highly intuitive visual for demonstrating covariate balance improvement.
- Explicitly shows which repos are being compared (pedagogically
  transparent).

**Fit with this dataset**:
- **Good**: The 604-repo dataset has strong covariate imbalance
  (creation year SMD = 0.75), so matching will visibly trim the sample
  and improve balance. This is pedagogically dramatic.
- **Limitation**: Same conditional ignorability assumption as OLS — it
  can only adjust for observables. The three OVB tools already show this
  is insufficient. But demonstrating this explicitly is the point.

**Implementation**: Use `MatchIt` in R (nearest-neighbor 1:1 matching on
propensity score from logistic regression on log_ncloc, log_commits,
log_stars, creation_year, framework). Report: (a) propensity score
distribution by language, (b) love plot, (c) ATT estimates on matched
sample for each outcome, (d) comparison with OLS.

### 2. Inverse Probability Weighting (IPW)

**What it does**: Re-weights the full sample so that the covariate
distribution of JS repos looks like that of TS repos (or vice versa),
using the inverse of the estimated propensity score as weights.

**What it adds beyond current OLS**:
- Retains all observations (no trimming) but re-weights them.
- Shows that different re-weighting estimators (ATE vs. ATT) can produce
  different answers on the same data.
- Effective sample size (ESS) diagnostic reveals how much information
  extreme weights discard.

**Fit with this dataset**:
- **Moderate**: With strong imbalance, some JS repos will get extreme
  weights (young, large, popular JS repos that "look like" TS). This
  illustrates a real practical problem and motivates weight trimming.
- The result will likely be similar to OLS and PSM, reinforcing the
  message that all selection-on-observables methods hit the same ceiling.

**Implementation**: Fit propensity score model; compute IPW weights for
ATT; estimate weighted OLS; report effective sample size and compare
with unweighted OLS. Could use `WeightIt` + `cobalt` packages.

### 3. Synthetic Control Method (SCM)

**What it does**: Constructs a synthetic version of a treated unit as a
weighted combination of control (donor) units, choosing weights to match
the treated unit's pre-treatment trajectory. Primarily designed for
comparative case studies with few treated units and many time periods.

**Fit with this dataset**:
- **Poor for the current cross-sectional data**. SCM requires panel data
  with a pre-treatment period and a post-treatment intervention point.
  The Bogner & Merkel data is a single cross-sectional snapshot — there
  is no temporal dimension to construct pre-treatment fit or observe
  post-treatment divergence.
- A synthetic control analysis would require fundamentally different data:
  e.g., monthly/quarterly quality metrics for specific repos that
  migrated from JS to TS, with donor repos that did not migrate. This is
  essentially the longitudinal panel data that Stage 4 already motivates
  as the next step.
- **However**, a variant — "synthetic matching" or Synthetic DID
  (Arkhangelsky et al. 2021) — could be applied if we had panel data.
  This is worth noting in the plan as a future direction.

**Recommendation**: Do **not** implement SCM on the current
cross-sectional data. Instead, note in the narrative that SCM is designed
for panel settings and that its application would require the longitudinal
data collection discussed in Stage 4.

---

## Recommended Approach: Add a New Stage 2.5

Insert a new analysis section between the current Stage 2 (OVB
assessment) and Stage 3 (within-TS dose-response). This positions
matching and IPW as the natural "what if we try harder to balance on
observables?" response to the OVB diagnosis, before pivoting to the
sharper treatment design.

### Stage 2.5: Selection-on-Observables Methods

#### Tasks

- [ ] **2.5a. Propensity score estimation and overlap assessment**
  - Fit a logistic regression: `is_ts ~ log_ncloc + log_commits +
    log_stars + creation_year + framework`.
  - Plot the estimated propensity score distribution by language
    (overlapping histograms or density plots). Look for overlap
    violations — JS repos with near-zero propensity, TS repos with
    near-one propensity.
  - Report common support statistics: what fraction of repos fall in the
    region of overlap?
  - **Pedagogical point**: If the propensity score distributions barely
    overlap, no amount of matching or weighting can make JS and TS repos
    comparable — we are extrapolating, not interpolating.

- [ ] **2.5b. Propensity score matching (PSM)**
  - Use `MatchIt` with nearest-neighbor 1:1 matching without replacement
    on the estimated propensity score.
  - Produce a **love plot** showing SMDs before and after matching for
    all covariates. Target: all post-matching SMDs < 0.1.
  - Report the number of matched pairs (sample attrition from matching).
  - Estimate the ATT for each of the four outcomes on the matched sample
    using OLS with HC1 robust SEs.
  - Sensitivity check: repeat with caliper matching (caliper = 0.2 SD
    of logit propensity score) and with full matching (optimal full
    matching via `MatchIt`). Report if conclusions differ.

- [ ] **2.5c. Inverse probability weighting (IPW)**
  - Compute IPW weights for the ATT estimand using the propensity score.
  - Report the effective sample size (ESS) to show how much extreme
    weights reduce the information content.
  - Estimate the ATT using weighted OLS for each outcome.
  - Compare: unweighted OLS (M5), PSM, and IPW side-by-side. If all
    three give similar estimates, this reinforces the message: the
    method of adjustment is not the bottleneck — the bottleneck is
    unobserved confounding.

- [ ] **2.5d. Re-apply OVB diagnostics to matched/weighted estimates**
  - Run `sensemakr` on the matched sample (post-matching OLS). Report
    robustness values.
  - The key comparison: did matching move the RV meaningfully? If not,
    the OVB problem is not about functional form or poor balance on
    observables — it is about missing variables.

- [ ] **2.5e. Summary table and pedagogical narrative**
  - Produce a combined table:

    | Method | Code smells coef | SE | p | N |
    |---|---|---|---|---|
    | M0: Unadjusted OLS | -0.0122 | 0.0016 | <0.001 | 604 |
    | M5: Adjusted OLS | -0.0044 | 0.0015 | 0.004 | 604 |
    | PSM (1:1 NN) | ? | ? | ? | ? |
    | IPW (ATT) | ? | ? | ? | ? |

  - Write narrative connecting OLS → matching → IPW → OVB: all three
    selection-on-observables methods agree (or disagree), illustrating
    that the identifying assumption — not the estimator — is the
    binding constraint.
  - Note that PSM, IPW, and OLS are three estimators for the same
    estimand under the same assumption. If they disagree, it signals
    model misspecification; if they agree, it means the estimand is
    well-estimated *conditional on the assumption holding*, but the
    assumption itself (conditional ignorability given observables) is
    the weak link, as the OVB diagnostics already demonstrated.

- [ ] **2.5f. Note on synthetic control**
  - Add a short paragraph explaining that SCM requires a panel structure
    (pre/post treatment trajectories) and is not applicable to
    cross-sectional data.
  - Reference Abadie et al. (2010) and Synthetic DID (Arkhangelsky
    et al. 2021) as the appropriate framework if longitudinal data were
    available.
  - This reinforces the Stage 4 motivation for collecting panel data.

### Why Not CEM (Coarsened Exact Matching)?

CEM is another matching method that coarsens covariates into bins and
matches exactly on coarsened values. It is attractive for its simplicity
but would likely discard too many observations given the strong imbalance
on creation year and stars (the coarsened bins may have no overlap in
extreme regions). Mention as a robustness check if space permits, but
PSM is more pedagogically central.

---

## Relationship to Existing Stages

The new stage slots into the existing notebook structure:

1. Stage 1: Diagnostic (unchanged)
2. Stage 2: OLS + OVB (unchanged)
3. **Stage 2.5: PSM + IPW (NEW)** ← this plan
4. Stage 3: Within-TS dose-response (unchanged, but renumbered to 3)
5. Stage 4: Bridge to longitudinal data (unchanged, but renumbered to 4)

The punchline of Stage 2.5 feeds directly into Stage 3: since all
selection-on-observables methods hit the same ceiling, the natural next
step is not a better estimator but a better *design* — which is what
the within-TS reframing provides, and what the longitudinal panel data
would provide even more forcefully.

---

## Pedagogical Value for the Paper

Adding matching and IPW serves three purposes in the tutorial paper:

1. **Demonstrates the method**: Readers learn *how* to implement PSM and
   IPW in R, including diagnostics (love plots, overlap, ESS).
2. **Illustrates the "same-assumption" lesson**: Matching, IPW, and OLS
   all require conditional ignorability. Showing they produce similar
   estimates and then showing (via sensemakr) that all are equally fragile
   is the most powerful way to teach this insight.
3. **Motivates design-based methods**: The convergence of all
   selection-on-observables methods at the same fragile estimate creates
   the strongest possible motivation for pivoting to a fundamentally
   different identification strategy (fixed effects, DiD, IV).

---

## R Packages Needed

- `MatchIt` — propensity score matching
- `cobalt` — balance diagnostics and love plots
- `WeightIt` — IPW weight estimation
- `survey` or `estimatr` — weighted regression with robust SEs
- `sensemakr` — already loaded; re-use for post-matching sensitivity

---

## Implementation Notes

- Use the same analysis frame (`df`) from the existing notebook.
- The propensity score model should use the same covariates as the OLS
  fully adjusted model (M5): `log_ncloc`, `log_commits`, `log_stars`,
  `creation_year`, `framework`.
- For the love plot, use `cobalt::love.plot()` with the Linux Libertine
  theme and 8×3 dimensions for consistency with existing figures.
- All robust SEs should use HC1 for consistency with existing tables.
- Report both statistical significance and the magnitude of coefficient
  change relative to OLS, since the pedagogical point is about the
  *convergence* of estimates, not just p-values.

---

## Estimated Scope

- **Code**: ~150-200 lines of R added to the notebook.
- **Narrative**: ~1 page in the paper (Section 4.4, between the OVB
  diagnosis and the within-TS design improvement).
- **Figures**: 2 new (propensity score overlap plot, love plot).
- **Tables**: 1 new (comparison of OLS, PSM, IPW estimates).

---

## Open Questions

1. **Should we feature all four outcomes or lead with one?** The
   existing notebook reports all four metrics. For matching/IPW, we
   could focus on code smells/nLOC (the lead outcome) to keep the
   presentation tight, with the others in a supplementary table.

2. **Full matching vs. 1:1 matching?** Full matching retains all units
   and is statistically more efficient, but 1:1 NN matching is more
   intuitive for a tutorial. Consider showing 1:1 as the primary
   analysis with full matching as a robustness check.

3. **Should the paper include both matching and IPW, or just one?**
   If space is tight, PSM alone suffices — it is more visual and
   intuitive. IPW adds value by showing a different estimator under
   the same assumption, but is less essential for the pedagogical arc.
