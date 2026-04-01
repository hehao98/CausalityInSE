# Plan: Matching, IPW, and Synthetic Control for MSR22 Reanalysis

## Context and Motivation

The current `notebooks/msr22_reanalysis.Rmd` implements a four-stage
progression on the Bogner & Merkel (MSR 2022) JS-vs-TS dataset (604 repos:
299 JS, 305 TS):

1. **Stage 1** — Replicate raw comparison; document covariate imbalance
   (SMDs: nLOC 0.06, commits 0.17, stars 0.40, creation year 0.75).
   DAG-guided covariate selection classifies each variable's role for the
   *code quality* outcome: `creation_year` and `framework` are confounders,
   `log_ncloc` is a confounder with minor post-treatment ambiguity,
   `log_commits` is post-treatment, and `log_stars` has both confounder
   and collider components.
2. **Stage 2** — OLS under two specifications (DAG-justified M_dag vs.
   kitchen-sink M_all) + three OVB diagnostics. Key finding: conditioning
   on stars attenuates the code smells coefficient by 32% (−0.0065 →
   −0.0044) and halves the robustness value (14.1% → 8.9%), consistent
   with collider bias.
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

## Critical DAG-Related Design Decision

The DAG analysis in Section 1.3 of the notebook established that GitHub
stars is ambiguous (confounder + collider) and log(commits) is
post-treatment. This has direct implications for matching and IPW:

**Which covariates should the propensity score model use?**

The propensity score should be estimated using only the DAG-justified
confounders: `log_ncloc + creation_year + framework`. Including
`log_stars` or `log_commits` in the propensity score would propagate
the same collider/post-treatment bias into the matching and weighting
estimators — defeating the purpose of using a DAG.

This creates a natural **two-specification comparison** for matching
and IPW, parallel to the OLS analysis:
- **DAG-justified PSM/IPW**: propensity score on `log_ncloc +
  creation_year + framework`
- **Kitchen-sink PSM/IPW**: propensity score on all five covariates

If both specifications agree, the collider issue does not affect
matching/IPW conclusions. If they disagree, it reinforces the lesson
that covariate selection matters for *all* selection-on-observables
methods, not just OLS.

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
  can only adjust for observables. The OVB tools already show this
  is insufficient. But demonstrating this explicitly is the point.

**Implementation**: Use `MatchIt` in R (nearest-neighbor 1:1 matching on
propensity score from logistic regression on DAG-justified covariates:
log_ncloc, creation_year, framework). Report: (a) propensity score
distribution by language, (b) love plot, (c) ATT estimates on matched
sample for each outcome, (d) comparison with M_dag OLS.

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
  weights (young, large JS repos that "look like" TS). This illustrates
  a real practical problem and motivates weight trimming.
- The result will likely be similar to OLS and PSM, reinforcing the
  message that all selection-on-observables methods hit the same ceiling.

**Implementation**: Fit propensity score model on DAG-justified
covariates; compute IPW weights for ATT; estimate weighted OLS; report
effective sample size and compare with M_dag OLS. Could use `WeightIt`
+ `cobalt` packages.

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
  - Fit **two** logistic regressions:
    - DAG-justified: `is_ts ~ log_ncloc + creation_year + framework`
    - Kitchen-sink: `is_ts ~ log_ncloc + log_commits + log_stars +
      creation_year + framework`
  - Plot the estimated propensity score distribution by language for
    both specifications (overlapping density plots). Look for overlap
    violations — JS repos with near-zero propensity, TS repos with
    near-one propensity.
  - Report common support statistics: what fraction of repos fall in the
    region of overlap? The kitchen-sink PS (including stars) will likely
    show *better* separation between JS and TS, which sounds good for
    prediction but is *bad* for causal inference — it means stars is so
    strongly associated with treatment that it dominates the PS, and the
    PS is partly capturing the collider pathway.
  - **Pedagogical point**: If the propensity score distributions barely
    overlap, no amount of matching or weighting can make JS and TS repos
    comparable — we are extrapolating, not interpolating.

- [ ] **2.5b. Propensity score matching (PSM)**
  - Primary analysis: Use `MatchIt` with nearest-neighbor 1:1 matching
    without replacement on the **DAG-justified** propensity score.
  - Produce a **love plot** showing SMDs before and after matching for
    the DAG-justified covariates plus stars and commits (to show whether
    matching on confounders also improves balance on the excluded
    variables).
  - Report the number of matched pairs (sample attrition from matching).
  - Estimate the ATT for each of the four outcomes on the matched sample
    using OLS with HC1 robust SEs.
  - Robustness: repeat with kitchen-sink PS. Compare ATT estimates.
    If they differ, the difference is attributable to the collider
    variable's influence on the propensity score.
  - Additional robustness: caliper matching (caliper = 0.2 SD of logit
    propensity score) and full matching (optimal full matching via
    `MatchIt`).

- [ ] **2.5c. Inverse probability weighting (IPW)**
  - Compute IPW weights for the ATT estimand using the DAG-justified
    propensity score.
  - Report the effective sample size (ESS) to show how much extreme
    weights reduce the information content.
  - Estimate the ATT using weighted OLS for each outcome.
  - Robustness: repeat with kitchen-sink PS weights.
  - Compare: M_dag OLS, DAG-justified PSM, DAG-justified IPW side-by-side.

- [ ] **2.5d. Re-apply OVB diagnostics to matched/weighted estimates**
  - Run `sensemakr` on the matched sample (post-matching OLS on
    DAG-justified covariates). Report robustness values.
  - The key comparison: did matching move the RV meaningfully compared
    to M_dag OLS? If not, the OVB problem is not about functional form
    or poor balance on observables — it is about missing variables.
  - This is the strongest version of the "same-assumption" lesson:
    three different estimators, same robustness value, same fragility.

- [ ] **2.5e. Summary table and pedagogical narrative**
  - Produce a combined table:

    | Method | Code smells coef | SE | p | N | RV |
    |---|---|---|---|---|---|
    | M0: Unadjusted OLS | −0.0122 | 0.0016 | <0.001 | 604 | — |
    | M_dag: DAG-justified OLS | −0.0065 | 0.0018 | <0.001 | 604 | 14.1% |
    | M_all: Kitchen-sink OLS | −0.0044 | 0.0020 | 0.004 | 604 | 8.9% |
    | PSM (DAG-justified, 1:1 NN) | ? | ? | ? | ? | ? |
    | IPW (DAG-justified, ATT) | ? | ? | ? | ? | ? |
    | PSM (kitchen-sink, 1:1 NN) | ? | ? | ? | ? | ? |

  - Write narrative connecting the DAG exercise to matching/IPW:
    - The DAG tells us *which* covariates to include in the propensity
      score — the same collider/post-treatment issues apply to matching
      and IPW as to OLS.
    - All selection-on-observables methods (OLS, PSM, IPW) under the
      DAG-justified specification should agree. If they do, the estimand
      is well-estimated *conditional on the assumption holding*. But
      the assumption (conditional ignorability given observables) is the
      weak link, as the OVB diagnostics show.
    - The convergence of all methods at a fragile estimate creates the
      strongest possible motivation for pivoting to a design-based
      strategy.

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
on creation year (the coarsened bins may have no overlap in extreme
regions). Mention as a robustness check if space permits, but PSM is
more pedagogically central.

---

## Relationship to Existing Stages

The new stage slots into the existing notebook structure:

1. Stage 1: Diagnostic + DAG-guided covariate selection (unchanged)
2. Stage 2: DAG-justified vs. kitchen-sink OLS + OVB (unchanged)
3. **Stage 2.5: PSM + IPW (NEW)** ← this plan
4. Stage 3: Within-TS dose-response (unchanged)
5. Stage 4: Bridge to longitudinal data (unchanged)

The punchline of Stage 2.5 feeds directly into Stage 3: since all
selection-on-observables methods hit the same ceiling, the natural next
step is not a better estimator but a better *design* — which is what
the within-TS reframing provides, and what the longitudinal panel data
would provide even more forcefully.

---

## Pedagogical Value for the Paper

Adding matching and IPW serves four purposes in the tutorial paper:

1. **Demonstrates the method**: Readers learn *how* to implement PSM and
   IPW in R, including diagnostics (love plots, overlap, ESS).
2. **Extends the DAG lesson to matching**: The same DAG that guided
   covariate selection for OLS also guides the propensity score model.
   Showing that the kitchen-sink propensity score produces different
   matches (and different estimates) than the DAG-justified one reinforces
   that DAG reasoning applies to *all* selection-on-observables methods.
3. **Illustrates the "same-assumption" lesson**: Matching, IPW, and OLS
   all require conditional ignorability. Showing they produce similar
   estimates (under the same covariate set) and then showing (via
   sensemakr) that all are equally fragile is the most powerful way to
   teach this insight.
4. **Motivates design-based methods**: The convergence of all
   selection-on-observables methods at the same fragile estimate creates
   the strongest possible motivation for pivoting to a fundamentally
   different identification strategy (fixed effects, DiD, IV).

---

## R Packages Needed

- `MatchIt` — propensity score matching
- `cobalt` — balance diagnostics and love plots
- `WeightIt` — IPW weight estimation (optional; can compute manually)
- `survey` or `estimatr` — weighted regression with robust SEs
- `sensemakr` — already loaded; re-use for post-matching sensitivity

---

## Implementation Notes

- Use the same analysis frame (`df`) from the existing notebook.
- **Primary propensity score model**: DAG-justified covariates only
  (`log_ncloc`, `creation_year`, `framework`). This is consistent with
  the DAG reasoning in Section 1.3.
- **Secondary propensity score model**: Kitchen-sink covariates (add
  `log_commits`, `log_stars`). This is for the DAG vs. kitchen-sink
  comparison.
- For the love plot, use `cobalt::love.plot()` with the Linux Libertine
  theme and 8×3 dimensions for consistency with existing figures.
- All robust SEs should use HC1 for consistency with existing tables.
- Report both statistical significance and the magnitude of coefficient
  change relative to M_dag OLS, since the pedagogical point is about
  the *convergence* of estimates, not just p-values.

---

## Estimated Scope

- **Code**: ~150-200 lines of R added to the notebook.
- **Narrative**: ~1 page in the paper (Section 4.4, between the OVB
  diagnosis and the within-TS design improvement).
- **Figures**: 2-3 new (propensity score overlap plot, love plot,
  possibly a comparison forest plot).
- **Tables**: 1 new (comparison of M_dag OLS, PSM, IPW estimates with
  RVs).

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

4. **Resolved: Which covariates for the propensity score?**
   Use DAG-justified covariates as primary, kitchen-sink as robustness.
   This is consistent with the DAG analysis and creates a parallel
   structure with the OLS comparison in Stage 2.
