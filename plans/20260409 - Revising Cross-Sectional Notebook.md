# Revising Cross-Sectional Notebook for Section 4.1

**Created:** 2026-04-09
**Supersedes:** 20260401 - Cross-Sectional AI Coding Tool Example Plan.md
(Phase 1 data collection is complete; this plan covers only the notebook
revision for the paper write-up.)

---

## Goal

Revise `notebooks/ai_adoption_cross_sectional.Rmd` so that it produces
exactly the tables, figures, and narrative needed for Section 4.1 of the
paper.  The new story follows a three-stage arc:

1. Start from what a typical SE researcher would do (naive comparison,
   kitchen-sink regression).
2. Diagnose why it fails (temporal collapse, sensitivity analysis).
3. Show that switching estimators cannot help (OLS/PSM/IPW convergence).

The central new idea is **temporal collapse**: MSR snapshot data merges
pre-treatment and post-treatment states of time-varying covariates into a
single node, destroying the acyclicity that DAGs require and making
covariate selection incoherent.  This replaces the old "confounder vs.
mediator ambiguity" framing.

---

## Mapping: Current Notebook → Revised Notebook

### What to keep (with modifications)

| Current section | What it produces | Disposition |
|---|---|---|
| Setup + Load Data (lines 1--118) | Package loading, data prep, treatment/outcome variables | **Keep as-is.** |
| §1.3 SMD computation + `compute_smd()` (lines 186--244) | SMD calculation infrastructure | **Keep** the function; fold SMDs into the new Table 1 instead of a standalone table/plot. |
| §2.1 OLS models (lines 325--376) | Three OLS specs (M_pretreat, M_extended, M_all) + extraction function | **Keep** `extract_treated()` and `m_pretreat`. **Drop M_extended** as a named specification. Rename `m_all` to `m_kitchen` and present it first. |
| §2.2 Coefficient stability plot (lines 392--444) | Progressively richer models plotted | **Keep and relabel.** Highlight kitchen-sink and M_pretreat only (blue/orange shading). Drop M_extended shading. |
| §2.3 sensemakr on M_pretreat (lines 469--481) | Sensitivity analysis + contour plot | **Keep.** This is the defensible specification. |
| §2.4 Oster bounds function (lines 514--536) | `oster_delta()` helper | **Keep** the function; compute only `bivariate → M_pretreat`. |
| §3.1--3.4 PSM + IPW code (lines 600--672) | Matching, weighting, estimation | **Keep** but switch covariates from M_extended to pre-treatment only. |
| §3.5 Three-estimator comparison table + plot (lines 677--715) | Convergence demonstration | **Keep** with updated covariate set and labels. |

### What to cut

| Current section | Why cut |
|---|---|
| §1.1 `maturity_distribution` table (lines 124--131) | Treatment definition detail; mention in prose, not a standalone table. |
| §1.1 `maturity_by_language` crosstab (lines 133--147) | Same; fold language distribution into Table 1 or a brief prose note. |
| §1.2 `outcome_comparison` density plot (lines 151--167) | Nice but not paper-ready; Table 1 descriptive stats are sufficient. |
| §1.2 `outcome_summary` table (lines 169--182) | Replaced by Table 1. |
| §1.3 SMD dot plot (lines 224--235) | Replaced by SMD column in Table 1. |
| §1.3 standalone SMD table (lines 237--244) | Replaced by Table 1. |
| §1.4 interpretation prose (lines 246--302) | Entire "clean confounders / ambiguous / likely proxies / unobserved" classification is replaced by temporal collapse framing. |
| §2.1 M_extended model and its row in the OLS table | M_extended was built for the old "confounder vs. mediator" framing. Under temporal collapse, the story is simpler: pre-treatment vs. kitchen-sink. |
| §2.3 sensemakr on M_extended (lines 483--491) | Uninterpretable under temporal collapse; M_extended is not a defensible specification. |
| §2.4 Oster `bivariate → M_extended` and `M_pretreat → M_extended` (lines 541--555) | Same reason. |
| §2.4 Oster interpretation prose about M_extended comparisons (lines 568--587) | Replaced by simpler interpretation. |
| §3.2 `love.plot` balance after matching (lines 614--621) | Diagnostic detail; Stage 3's point is convergence, not matching quality. |
| §4 "cross-sectional ceiling" prose + summary table (lines 717--825) | Rewrite entirely around temporal collapse; drop "Example C (Cursor ITS/DiD)" references — the bridge now goes to Section 4.2. |

### What to add

| New element | Purpose | Placement |
|---|---|---|
| **Table 1: Descriptive comparison** | One unified table: variable name, control mean, treated mean, SMD — for outcome + all covariates (pre-treatment and time-varying). Annotate rows as "pre-treatment" or "time-varying" in a column or with visual grouping. | Stage 1 |
| **Kitchen-sink OLS as the opening regression** | Present kitchen-sink *first* as what a naive analyst would do. Coefficient is large and significant. "A naive analyst might stop here." | Stage 1 |
| **Temporal collapse discussion** | Prose section explaining: (a) the true temporal DAG (stars_{t-1} → adoption_t, etc.), (b) how a snapshot collapses it into a cyclic graph, (c) consequence: only structurally pre-treatment covariates are defensible. Reference figure placeholders for the paper's TikZ DAG diagrams. | Stage 2 |
| **Covariate classification table** | Small table: each covariate tagged as "structurally pre-treatment" or "temporally ambiguous" with one-line justification. | Stage 2 |
| **PSM/IPW with pre-treatment covariates** | Currently uses M_extended covariates. Switch propensity score formula to `treated ~ repo_age_yr + queried_language + is_org`. | Stage 3 |

---

## Revised Notebook Structure

```
# Setup + Load Data
  (keep as-is)

# Stage 1: What Would a Typical SE Researcher Do?

## 1.1 Descriptive Comparison (Table 1)
  - One table: rows = outcome + all covariates, columns = control
    mean, treated mean, SMD.  Rows grouped or annotated by temporal
    status (pre-treatment vs. time-varying).
  - Brief prose: treatment prevalence, language distribution, the
    5.8x raw gap.

## 1.2 Kitchen-Sink Regression
  - m_kitchen: regress log(monthly commits) on treated + all
    covariates (age, language, org, CI, size, releases, stars,
    forks, PRs, issues).
  - Report coefficient, robust SE, p-value, R².
  - Narrative: "The coefficient is large, highly significant, and
    survives a battery of controls.  A naive analyst might conclude
    that AI adoption causes higher productivity.  But should we
    trust this?"

# Stage 2: Why Should We Distrust This?

## 2.1 The Temporal Collapse Problem
  - Prose: introduce the true temporal DAG for this setting.
    stars_{t-1} → adoption_t, stars_{t-1} → commits_t,
    adoption_t → stars_{t+1}, commits_t → stars_{t+1}.
    Covariate roles are unambiguous.
  - Prose: show what a cross-sectional snapshot does — collapses
    time-indexed nodes into a single "stars" node that is
    simultaneously a confounder and a collider.  The resulting
    graph is cyclic, not a DAG.
  - Reference the paper's TikZ figures (to be drawn in LaTeX).
  - Connect to Hernán & Robins (Ch. 20) treatment-confounder
    feedback and Richardson & Robins' critique of cross-sectional
    DAGs.

## 2.2 Covariate Classification
  - Small table classifying each covariate:
    | Covariate | Temporal status | Justification |
    | Repo age | Pre-treatment | Determined at creation |
    | Language | Pre-treatment | Determined at creation |
    | Org type | Pre-treatment | Determined at creation |
    | Stars | Temporally ambiguous | Accumulate before and after adoption |
    | Forks | Temporally ambiguous | Same |
    | CI/CD | Temporally ambiguous | May be adopted as part of same modernization wave |
    | Repo size | Temporally ambiguous | Includes post-adoption code growth |
    | Releases | Temporally ambiguous | Includes post-adoption releases |
    | PRs | Temporally ambiguous | Same |
    | Issues | Temporally ambiguous | Same |
  - Consequence: only age, language, and org type are defensible
    controls. Restricting to pre-treatment covariates eliminates
    mediator bias entirely and reduces collider risk to the minor
    M-bias scenario.

## 2.3 Pre-Treatment vs. Kitchen-Sink OLS (Table 2)
  - Table with three rows: bivariate, M_pretreat, kitchen-sink.
    Columns: coefficient, robust SE, p-value, R².
  - Coefficient stability plot (keep from current §2.2, relabel).
    Highlight M_pretreat (blue) and kitchen-sink (orange).
  - Key narrative: the drop from M_pretreat to kitchen-sink is
    *uninterpretable* — the collapsed graph is not a DAG, so no
    adjustment formula applies.  Even the bivariate → M_pretreat
    drop, though defensible, leaves a large residual.

## 2.4 Sensitivity Analysis
  - sensemakr on M_pretreat only.  One summary, one contour plot.
  - Oster bounds: bivariate → M_pretreat only.
  - Interpretation: the pre-treatment covariates are weak proxies
    for the real confounders (developer skill, team culture).
    delta* is large but misleading — it reflects how uninformative
    the pre-treatment covariates are, not how safe the estimate is.

# Stage 3: Can a Better Estimator Help?

## 3.1 PSM and IPW with Pre-Treatment Covariates
  - Propensity score formula: treated ~ repo_age_yr +
    queried_language + is_org  (pre-treatment only).
  - PSM: 1:1 nearest-neighbor matching.
  - IPW: ATT weights.
  - Brief note on effective sample size.

## 3.2 Three-Estimator Comparison (Table 3)
  - Table: OLS (M_pretreat), PSM, IPW — coefficient, robust SE,
    p-value, N.
  - Convergence plot (keep from current §3.5, relabel).
  - Narrative: "All three share the same identifying assumption
    (conditional ignorability given pre-treatment covariates) and
    that assumption is violated.  Switching the estimator changes
    nothing."

# Synthesis: The Cross-Sectional Ceiling

  - Rewrite around temporal collapse as the central argument.
  - Three-point summary:
    1. The raw gap is enormous, but temporal collapse makes DAG-based
       covariate selection incoherent for time-varying covariates.
    2. Restricting to pre-treatment covariates is defensible but yields
       fragile estimates — the covariates are weak proxies for the
       real confounders.
    3. The estimator is not the bottleneck — OLS, PSM, and IPW
       converge.
  - Bridge to Section 4.2: only within-repo longitudinal variation
    can make progress.
  - Updated summary table (three stages, not four).
```

---

## Task Checklist

### Stage 1 revisions
- [ ] Replace §1.1--§1.3 tables/plots with unified Table 1 (outcome + all
      covariates, by group, with SMD column and temporal status annotation)
- [ ] Move kitchen-sink OLS (`m_all` → `m_kitchen`) to Stage 1 as the
      naive baseline; write "naive analyst" framing prose
- [ ] Cut: maturity distribution table, maturity-by-language crosstab,
      outcome density plot, standalone SMD dot plot and SMD table

### Stage 2 revisions
- [ ] Write temporal collapse prose section (true temporal DAG vs.
      collapsed cross-sectional graph; Hernán & Robins / Richardson &
      Robins references)
- [ ] Create covariate classification table (pre-treatment vs. temporally
      ambiguous)
- [ ] Restructure OLS table: bivariate, M_pretreat, kitchen-sink (drop
      M_extended row)
- [ ] Relabel coefficient stability plot (highlight M_pretreat and
      kitchen-sink only; remove M_extended shading)
- [ ] Cut sensemakr on M_extended; keep only M_pretreat run + contour plot
- [ ] Cut Oster bivariate→M_extended and M_pretreat→M_extended; keep only
      bivariate→M_pretreat
- [ ] Rewrite §1.4 interpretation prose entirely (replace "clean /
      ambiguous / likely proxies" with temporal collapse framing)

### Stage 3 revisions
- [ ] Change PSM/IPW propensity score formula from M_extended covariates
      to pre-treatment only (`treated ~ repo_age_yr + queried_language +
      is_org`)
- [ ] Update three-estimator comparison table and plot labels
- [ ] Cut love.plot (balance after matching)

### Synthesis revisions
- [ ] Rewrite Stage 4 prose around temporal collapse (drop "Example C
      (Cursor ITS/DiD)" references; bridge to Section 4.2)
- [ ] Update summary table for three-stage structure

### Header and preamble
- [ ] Rewrite notebook title and introductory prose to reflect new
      three-stage arc and temporal collapse framing
- [ ] Remove references to "four-stage structure from Bogner & Merkel
      reanalysis"

---

## Paper Artifacts Produced by This Notebook

After revision, the notebook should produce exactly these artifacts for
inclusion in Section 4.1 of the paper:

| Artifact | Type | Content |
|---|---|---|
| Table 1 | Table | Descriptive comparison: outcome + covariates by group, with SMD and temporal status |
| Table 2 | Table | OLS comparison: bivariate, M_pretreat, kitchen-sink (coef, SE, p, R²) |
| Table 3 | Table | Estimator comparison: OLS, PSM, IPW with pre-treatment covariates |
| Figure 1 | Plot | Coefficient stability across specifications |
| Figure 2 | Plot | sensemakr contour plot for M_pretreat |

The temporal DAG figures (true temporal DAG and collapsed cross-sectional
graph) will be drawn in LaTeX/TikZ directly in the paper, not generated
by the notebook.  The notebook will reference them with placeholder text.
