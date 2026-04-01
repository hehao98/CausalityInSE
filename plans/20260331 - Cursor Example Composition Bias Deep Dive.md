# Cursor Example: Composition Bias Mechanisms and Compelling Story

**Date:** 2026-03-31
**Status:** Planning

## Background

The Cursor worked example (Example C) shows a sign flip: naive ITS without
repo FE suggests Cursor *improves* code quality, but repo FE reverses the
direction (quality *worsens* within-repo). The README attributes this to
"selection into treatment" — higher-quality repos adopted earlier. This plan
investigates the precise mechanisms behind the flip and proposes additional
analyses to make the pedagogical story maximally compelling.

## Mechanisms Behind the Sign Flip

Exploratory data analysis reveals **three layered mechanisms**, each
amenable to a distinct diagnostic analysis:

### Mechanism 1: New-Repo Contamination (Dominant)

265 of 830 treated repos appear **only in the post-period** — they have zero
pre-adoption observations within the ±6-month window. These are brand-new
repos (mean age ~20 days vs ~687 days for balanced repos) with trivially
clean codebases:

| Metric            | Post-only repos (265) | Balanced repos (565) |
|-------------------|-----------------------|----------------------|
| Mean code smells  | 93.7                  | 1,671.1              |
| Mean cog. complex.| 478.7                 | 6,260.1              |
| Mean nLOC         | 5,939                 | 63,704               |
| Mean age (days)   | 19.8                  | 686.7                |

These repos were likely **created alongside or immediately after Cursor
adoption** — developers starting new projects with Cursor from day one. In
the naive pooled pre/post comparison, their pristine quality metrics
contaminate the post-period mean, making it look like Cursor reduces code
smells and complexity. This is the primary driver of the spurious negative
level shift.

**Why this isn't about "older vs. newer repos" exactly:** The user's
intuition (pre has older repos, post has newer repos) is directionally right
but the mechanism is more specific. It isn't that calendar time shifts the
population — it's that brand-new repos that didn't exist before adoption
enter the sample exclusively in the post-period, and their trivially low
quality metrics create a mechanical composition shift.

### Mechanism 2: Staggered Adoption with Unbalanced Panel

Even among the 565 repos present in both pre and post periods, the panel is
internally unbalanced:

| Relative month | Repos present |
|----------------|---------------|
| -6             | 397           |
| -3             | 465           |
| -1             | 565           |
| 0              | 565           |
| +1             | 513           |
| +3             | 464           |
| +6             | 233           |

Repos enter and exit the window depending on when they adopted Cursor and
how much data exists before/after adoption. Early adopters (≤2024-10) are
systematically smaller and cleaner than late adopters:

- Early (N=90): mean code_smells=514, mean cog_complexity=2,289
- Late (N=484): mean code_smells=1,541, mean cog_complexity=6,039

This means early relative months (like -6) are over-represented by late
adopters (large, messy repos), while later relative months (like +6) are
over-represented by early adopters (small, clean repos). This creates a
second, subtler composition gradient that biases naive trend estimates even
within the balanced panel.

### Mechanism 3: Natural Code Aging (Confounding with Time)

Even on the fully balanced sub-panel (174 repos with all 13 months), quality
metrics *increase* from pre to post:

- Code smells: 2,070 → 2,198 (+6.2%)
- Cognitive complexity: 8,221 → 32,374 (+294%)

Some of this is likely the genuine Cursor effect, but some is natural code
growth — repos accumulate complexity as developers add features over time.
The treated-only ITS **cannot separate these two forces**. Only a
difference-in-differences design with matched control repos can difference
out secular time trends.

## Framing the Threat: Why Naive Pre/Post Fails

The naive pre/post comparison commits a **textbook Simpson's paradox**:

> **Aggregate:** Post-period has lower mean quality metrics than pre-period →
> "Cursor improves quality."
>
> **Within each repo:** Post-adoption quality metrics are higher than
> pre-adoption → "Cursor worsens quality."

The reversal is entirely explained by composition: the post-period is
flooded with 265 brand-new, trivially clean repos that didn't exist in the
pre-period. The aggregate comparison is a between-repo comparison
masquerading as a within-repo comparison.

This is a **powerful pedagogical device** because:
1. It is a real-world instance of Simpson's paradox in SE data, not a
   textbook hypothetical.
2. The naive conclusion ("AI improves code quality") is precisely the kind
   of claim that would get amplified in tech media and practitioner
   discourse.
3. The fix is conceptually simple (compare each repo to its own baseline),
   but requires the researcher to know about and implement fixed effects.

## Plan: Building the Most Compelling Story

The analysis should progress as a **layered reveal**, where each step
exposes a new threat and addresses it. This mirrors the pragmatic stance's
philosophy: identify threats to validity, then select designs that address
them.

### Step 1: Show the Naive Pre/Post Result (Already Done)

**What it shows:** Pooled comparison of pre vs. post observations suggests
Cursor has no significant effect on quality (or slightly improves it).

**Threat exposed:** None — this is the starting point.

### Step 2: Expose the Composition Bias Visually (NEW)

- [ ] **Analysis 2a: Repo count by relative month.** A simple bar chart or
  line plot showing how many repos contribute to each relative month. The
  jump from 565 at month -1 to 830 at month 0 makes the unbalanced panel
  immediately visible.

- [ ] **Analysis 2b: Characteristics of post-only repos.** A table or
  figure comparing the 265 post-only repos to the 565 balanced repos on key
  dimensions (age, nLOC, code smells, complexity). The 10-30× difference in
  every metric makes the contamination obvious.

- [ ] **Analysis 2c: Composition-weighted mean decomposition.** For the
  quality outcomes, decompose the pre-to-post change in the pooled mean into
  (a) within-repo change and (b) composition change (new repos entering).
  This is an Oaxaca-Blinder style decomposition or simply:
  ```
  Δ_pooled = Δ_within + Δ_composition
  ```
  Show that Δ_within is positive (quality worsens) but Δ_composition is
  negative (new clean repos enter) and dominates, making Δ_pooled negative
  (quality appears to improve).

**Threat exposed:** The sample composition changes between pre and post.

### Step 3: Restrict to Balanced Panel (NEW)

- [ ] **Analysis 3a: Re-run the naive pre/post on balanced panel only (565
  repos).** On the balanced panel, the spurious "quality improvement" should
  vanish or reverse. Show the sign either flips or becomes non-significant.

- [ ] **Analysis 3b: Re-run on fully balanced panel (174 repos with all 13
  months).** On the fully balanced panel, quality clearly degrades (code
  smells +6%, complexity +294%). The sign is already correct without FE.

**Threat exposed:** Composition bias was the primary driver. But the
balanced panel still has staggered-adoption composition drift (Mechanism 2)
and natural aging confounding (Mechanism 3).

### Step 4: Add Repo Fixed Effects (Already Done)

**What it shows:** Within-repo, quality worsens after Cursor adoption. The
sign flip from Step 1 is fully explained by composition.

**Threat exposed:** Repo FE removes time-invariant confounders (baseline
quality, project type, team experience). But it cannot distinguish the
Cursor effect from secular time trends (natural code aging). Any repo would
accumulate some complexity over 6 months regardless of Cursor.

### Step 5: Reference the Published DiD (Summary Only)

**What it shows:** The published MSR 2026 paper uses matched control repos
in a staggered DiD design. Control repos experience some code growth too,
but less than Cursor-adopting repos. Differencing out the control trend
confirms the within-repo quality degradation is partially attributable to
Cursor, not just natural aging.

**Threat addressed:** Secular time trends.

### Step 6 (Optional): Cohort Event Study Plot (NEW)

- [ ] **Analysis 6: Event study by adoption cohort.** Plot the mean quality
  trajectory separately for 3-4 adoption cohorts (e.g., Aug-Oct 2024,
  Nov-Dec 2024, Jan 2025, Feb-Mar 2025). If the trajectories look similar
  in event time despite occurring at different calendar times, it
  strengthens the case that the post-adoption quality increase is a
  treatment effect rather than a calendar-time artifact.

## What Changes in the Notebook

The existing `notebooks/msr26_reanalysis.Rmd` already has Steps 1 and 4.
The new analyses (Steps 2, 3, 6) should be inserted between them:

1. After the raw pre/post comparison, add a new section: **"Diagnosing
   Composition Bias"** (Analyses 2a, 2b, 2c).
2. After diagnosing composition bias, add: **"Restricting to a Balanced
   Panel"** (Analyses 3a, 3b).
3. Optionally, after the ITS section, add: **"Cohort Event Study"**
   (Analysis 6).

## How to Tell the Story in the Paper

The recommended narrative arc for the paper's Example C section:

1. **Setup:** "We have monthly panel data for 830 repos that adopted Cursor.
   A naive pre/post comparison suggests adoption has no significant effect
   on quality, or slightly improves it."

2. **First reveal (composition):** "But the sample composition changes
   dramatically between periods. 265 repos — brand-new projects created
   alongside Cursor adoption — appear only in the post-period. These repos
   have 10-30× fewer quality issues simply because they are tiny and young.
   Their presence in the post-period mechanically pulls down aggregate
   quality metrics."

3. **Second reveal (balanced panel):** "Restricting to the 565 repos
   observed in both periods, the quality 'improvement' vanishes. On the
   fully balanced sub-panel, quality clearly worsens."

4. **Third reveal (FE):** "Adding repo fixed effects — comparing each repo
   to its own pre-adoption baseline — confirms that quality deteriorates
   within-repo after Cursor adoption. The naive model got the sign exactly
   backwards."

5. **Remaining threat:** "Even the FE model cannot separate Cursor's effect
   from natural code aging. Only a control group (DiD) can. The published
   analysis confirms: Cursor-adopting repos accumulate quality issues faster
   than matched controls."

6. **Punchline:** "A naive pre/post comparison of AI tool adoption — the
   kind that populates tech blogs and could plausibly appear in a peer-
   reviewed study lacking causal methods — would conclude the opposite of
   what the data actually show. The composition bias is invisible unless you
   look for it."

This layered reveal is pedagogically superior to the current notebook
structure (which jumps from raw pre/post directly to ITS with four model
specifications) because it makes each threat *visible* before introducing
the method that addresses it.

## Task Checklist

- [ ] Implement Analysis 2a: repo count by relative month (bar chart)
- [ ] Implement Analysis 2b: post-only vs balanced repo comparison table
- [ ] Implement Analysis 2c: within vs composition decomposition
- [ ] Implement Analysis 3a: balanced-panel naive pre/post
- [ ] Implement Analysis 3b: fully balanced panel naive pre/post
- [ ] Implement Analysis 6: cohort event study plot (optional)
- [ ] Restructure notebook to follow layered-reveal narrative
- [ ] Update README Example C section with refined mechanism story
