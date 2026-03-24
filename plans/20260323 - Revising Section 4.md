# Plan: Revising Section 4 --- A Guide for Causal Inquiry in SE

**Decision:** We adopt Option B (decision-guided workflow with branching paths), reframed as a *guide* rather than a framework. The guide is self-contained and domain-neutral---it does not reference the PL--defect debate. The worked examples (Sections 5--6) revisit the guide to reinforce its points with concrete applications. The appendix contains a full-format ACM Empirical Standard for causal inquiry in SE---not just a checklist but a complete standard with Application scope, Specific Attributes (Essential / Desirable / Extraordinary), General Quality Criteria, Acceptable Deviations, Antipatterns, Invalid Criticisms, Suggested Readings, and Exemplars---designed to be directly proposed as a new standard in the ACM SIGSOFT Empirical Standards collection.

---

## Problem Statement

Section 3 delivers a dense primer spanning potential outcomes, DAGs, and design-based identification.
An SE researcher reading it for the first time may feel overwhelmed and unsure how to *apply* this material to their own work.
Section 4 must bridge the gap between conceptual foundations and practical research activity.

The current four-step framework has three problems:

1. **Prescriptiveness vs. creativity.** Causal inference is partly an art---the researcher must get creative in finding identification strategies that exploit the specific structure of their data and setting. A rigid "Step 1, 2, 3, 4" recipe obscures this and risks being treated as a bureaucratic checklist.
2. **Two fundamentally different paths.** The primer introduces two identification paradigms---selection-on-observables (DAG + back-door criterion) and design-based identification (DiD, IV, RDD, panel FE)---but the current framework conflates them into a single linear sequence without helping the researcher choose between them.
3. **Structural overlap with Section 3.** The current Section 4 opens with "Choosing Among Methods," "Internal--External Validity Trade-Off," and a "Pragmatic Stance" subsection that synthesize the primer rather than introduce something new. These belong in Section 3.

---

## Design Principles

- **Narrative function:** Section 4 is the *bridge* between "here is the toolkit" (Section 3) and "here is how we apply it" (Sections 5--6). It should feel like a trusted colleague walking the reader through the thinking process---honest that causal inference requires both creativity and extra care.
- **Self-contained and domain-neutral.** The guide must stand on its own without relying on the PL--defect running example. Examples within the guide should be brief, varied SE vignettes (code review, CI/CD adoption, language migration, tool mandates) that illustrate reasoning patterns without tying the guide to a single domain.
- **Dual audience.** (a) Researchers designing a new study, and (b) researchers or reviewers evaluating an existing study's causal claims. The guide should serve both.
- **Terminology.** Use "guide" throughout, not "framework." The word "guide" conveys structure and referencability while signaling that the researcher must exercise judgment. The appendix checklist is the concrete, mechanical counterpart.

---

## Prerequisite: Merging "Pragmatic Stance" Material into Section 3

The current Section 4 lines 619--667 contain three blocks that belong in Section 3:

| Block | Content |
|---|---|
| "Choosing Among Methods" | Different methods estimate different quantities; design-based methods have transparent assumptions; DAGs remain valuable alongside design-based methods |
| "Internal--External Validity Trade-Off" | Hierarchy of evidence; triangulation |
| "A Pragmatic Stance for SE Research" (current 4.1) | Three recommendations (use target trial reasoning, use DAGs, use design-based identification); why this fits SE |

**Action:** Merge these into Section 3.4 "A Pragmatic Stance for SE Research" (consistent with the Section 3 plan in `20260320 - Drafting Section 3.md`). The merged 3.4 should be revised to have a clear narrative arc:

1. **Open with the key tension.** The primer has laid out a rich but potentially overwhelming toolkit. The researcher now faces a practical question: *How do I actually use this?* Acknowledge honestly that there is no universal recipe---causal inference requires both methodological rigor and creative problem-solving.
2. **Three recommendations as a pragmatic synthesis.** Present the three recommendations (target trial reasoning, DAGs for mechanisms, design-based identification when possible) not as a checklist but as a *way of thinking* that integrates the three pillars. Emphasize that the researcher must assess the specific features of their data and setting---this is where domain expertise and methodological creativity intersect.
3. **Why this stance fits SE.** Four features of SE data make this synthesis particularly appropriate (unmeasured confounders in repository data, inherently panel-structured data, DAGs as natural for CS researchers, target trial bridges experiment tradition to observational settings).
4. **Close with the forward pointer.** Section 4 operationalizes this stance as a practical guide. The appendix provides a concrete checklist for structured assessment.

The tone should convey that the primer in Section 3 is the *vocabulary*; the pragmatic stance is the *grammar*; and Section 4 is the *conversation*---showing how to think in this language, not just recite it.

- [x] Revise and relocate "Choosing Among Methods," "Internal--External Validity," and current 4.1 into Section 3.4 with a clear narrative arc

---

## Section 4 Structure

> **Section 4: A Guide for Conducting Credible Causal Inquiry in SE**
>
> 4.1 Start with the Causal Question
> 4.2 Two Paths to Identification
>   - 4.2.1 Path A: DAG-Based Identification (Selection-on-Observables)
>   - 4.2.2 Path B: Design-Based Identification (Quasi-Experimental)
>   - 4.2.3 When Neither Path Is Clean
> 4.3 Probing Credibility: Limitations and Alternatives

---

## Detailed Content Plan

### 4.1 Start with the Causal Question

**Purpose:** The universal first move in any causal inquiry---articulate the question with precision. This is the non-negotiable foundation, regardless of what comes next.

**Content:**

- **Articulate the target trial.** Before touching data, describe the hypothetical randomized experiment you wish you could run. This forces clarity on: What is the treatment? What is the population? What is the outcome? What is the timing?
  - Brief SE vignette (not PL-specific): *"Suppose a researcher wants to know whether adopting continuous integration reduces post-release defects. The target trial would randomly assign teams to adopt CI and compare defect rates over the following year. Articulating this immediately reveals ambiguities: What counts as 'adopting CI'---a single pipeline or full integration? Which teams---greenfield or legacy? What defect metric---customer-reported or commit-linked?"*
- **Define the estimand.** State the causal quantity of interest (ATE, ATT, LATE) using the potential outcomes language from Section 3. Emphasize that choosing the estimand is a *substantive* decision reflecting the research question, not a statistical technicality.
- **Construct a preliminary DAG.** Even before choosing an identification strategy, sketch a DAG encoding the researcher's beliefs about the causal structure. This DAG immediately (a) surfaces confounders, mediators, and colliders, (b) reveals whether the treatment is well-defined or compound, and (c) makes assumptions visible for critique. The DAG will be refined as the researcher works through the identification strategy.
- **Emphasize iteration.** These three activities (target trial, estimand, DAG) are presented sequentially but are often iterative. Constructing the DAG may reveal that the treatment is poorly defined, sending the researcher back to reformulate the target trial. Defining the estimand may reveal that the question of interest (e.g., ATT vs. ATE) changes which identification strategy is feasible.

**Key message:** *Before you analyze, define what you are asking and what you are assuming about the world. Ambiguity in the causal question propagates into ambiguity in the conclusions.*

### 4.2 Two Paths to Identification

**Purpose:** The central creative act---finding an identification strategy that is credible given the data and setting. This is where causal inference becomes an art, and where the researcher must be both creative and extra careful.

**Opening framing paragraph:**
- The preliminary DAG from 4.1 reveals the confounders and mechanisms. The researcher now faces the key strategic question: *How will I argue that my estimate has a causal interpretation?*
- Two broad families of strategies exist, and the choice depends on the data structure and the plausibility of the required assumptions.
- Emphasize honestly: There is no algorithm for this choice. The researcher must assess the specific features of their data and setting. This is where domain expertise and methodological creativity intersect. A good causal study is not one that mechanically follows a recipe but one that *finds* an identification strategy that is credible in its specific context.

#### 4.2.1 Path A: DAG-Based Identification (Selection-on-Observables)

**When to use:** The researcher believes they can measure all important confounders identified in the DAG, or can argue persuasively that unmeasured confounders are negligible.

**Content:**
- Apply the back-door criterion to the DAG to identify the sufficient adjustment set.
- Choose an estimation method (regression, matching, IPW, doubly robust).
- Justify covariate selection explicitly using the DAG---not by "throwing in everything available." Every included variable should block a back-door path; every excluded variable should be justified (mediator, collider, or irrelevant).
- Conduct sensitivity analysis to probe vulnerability to unmeasured confounding (Rosenbaum bounds, E-values, robustness values, coefficient stability).

**Honest caveat:** In many SE settings, key confounders (developer skill, team culture, organizational practices) are unmeasurable from repository data. When the DAG reveals important unmeasured confounders, selection-on-observables is fragile and the researcher should consider Path B, combine approaches, or acknowledge the limitation prominently. Honesty about this fragility is itself a contribution---it clarifies the field's epistemic state.

**SE-specific guidance:**
- DAG-based identification works best when rich survey, organizational, or telemetry data is available (not just repository mining).
- Even with repository data, DAGs remain valuable for *justifying* which variables to include and exclude, even when full identification is not achieved.

#### 4.2.2 Path B: Design-Based Identification (Quasi-Experimental)

**When to use:** The data contain features that provide quasi-random variation in treatment assignment---temporal variation (panel data), staggered adoption (DiD), plausible instruments (IV), or assignment thresholds (RDD).

**Content:**
- Identify the quasi-experimental variation: What feature of the setting provides as-if-random variation in treatment? This is the creative step---the researcher must look at their data through the lens of "what natural experiments does this setting contain?"
- Match the variation to a method:

| Data Feature | Method | SE Example |
|---|---|---|
| Same units observed over time | Panel FE | Developers contributing in multiple languages across projects |
| Staggered adoption events | DiD | Teams adopting a linter at different times |
| External shock affecting treatment | IV | Platform policy mandating a practice |
| Threshold-based assignment | RDD | Eligibility for a program based on project size |

- State the method-specific assumptions (parallel trends, exclusion restriction, continuity at threshold, strict exogeneity) and argue for their plausibility using domain knowledge and the DAG from 4.1.
- Where possible, conduct partial tests (pre-trend tests for DiD, first-stage F-test for IV, McCrary density test for RDD).

**Honest caveat:** Design-based methods are not assumption-free. They replace the untestable "all confounders measured" with different assumptions that must be argued substantively. The DAG from 4.1 helps clarify which confounders the design absorbs and which remain as threats.

**SE-specific guidance:**
- SE data is *rich* in the temporal and structural variation that design-based methods exploit: repositories evolve over time, developers contribute across projects, tools are adopted in waves, platform policies create natural experiments.
- The researcher should actively seek these features in their data. A dataset that looks like a cross-section may, on closer inspection, contain panel structure or staggered adoption events that enable a much stronger design.

#### 4.2.3 When Neither Path Is Clean

**Purpose:** Honest acknowledgment that many SE settings do not neatly fit either path. This is not a failure---it is the norm.

**Content:**
- Sometimes the DAG reveals unmeasured confounders *and* no quasi-experimental variation is available. The researcher should:
  - Use the best available strategy (often DAG-based with careful sensitivity analysis).
  - Be transparent about the limitations and the direction of likely bias.
  - Frame conclusions as "consistent with a causal interpretation under assumptions X, Y, Z" rather than as definitive causal claims.
  - Consider whether the research question can be *reformulated* to exploit available variation. This reformulation is often the most creative and valuable act in a causal inquiry---it can transform an intractable question into a tractable one.
- Triangulation: Multiple imperfect approaches that converge on the same conclusion provide stronger evidence than any single approach.
- The pragmatic bottom line: *An honest, well-argued correlational analysis that explicitly states its identification limitations is more valuable than a spurious claim of causation.* Transparent uncertainty is a contribution; false certainty is a liability.

### 4.3 Probing Credibility: Limitations and Alternatives

**Purpose:** After choosing an identification strategy, the researcher must honestly assess its fragility and engage with rival explanations. This section absorbs the current Steps 3 and 4.

**Content --- Limitations:**
- No study achieves perfect identification, especially in SE where treatments are complex, key constructs lack universal definitions, and outcomes are proxied by noisy repository metrics.
- Limitations should be *mitigated*, not merely listed. A bare-bones "threats to validity" section that catalogues every conceivable problem without engaging with their severity or providing mitigation strategies fails the reader.
- Sensitivity analysis provides principled tools for quantifying fragility:
  - Rosenbaum bounds: How strong must an unmeasured confounder be to alter the conclusion?
  - Coefficient stability (Oster): Do point estimates shift substantially as controls are added?
  - Robustness values (Cinelli & Hazlett): What is the minimum confounder strength to nullify the result?
  - Pre-trend tests (DiD): Is the parallel trends assumption plausible?
  - Over-identification tests (IV): Are the exclusion restrictions credible?
- SE-specific measurement challenges: noisy proxies, construct validity issues, SUTVA violations in interconnected software ecosystems.

**Content --- Alternative Explanations:**
- Consider rival causal structures (alternative DAGs) that could generate the same observed patterns.
- Derive testable implications that discriminate among alternatives. The goal is not to eliminate all alternatives but to engage transparently with the most plausible ones.
- Three patterns of alternative explanations (illustrated with generic SE examples, not PL-specific):
  1. *Alternative mechanism:* The treatment effect operates through a different pathway than hypothesized. If so, conditioning on the alternative mediator should attenuate the effect.
  2. *Unmeasured confounding:* A hidden variable drives both treatment and outcome. Sensitivity analysis quantifies the required strength; falsification tests probe whether the confounding story predicts spurious effects on unrelated outcomes.
  3. *Reverse causality:* The outcome drives the treatment rather than the reverse. Panel data can reveal temporal signatures (e.g., does the outcome change *before* the treatment?).

**Key message:** *The mark of a credible causal study is not the absence of limitations but the transparency and rigor with which they are addressed.*

---

## Appendix: Causal Inquiry Empirical Standard

**Purpose:** A new empirical standard for SE studies making causal claims from observational data, written in the format of the [ACM SIGSOFT Empirical Standards](https://www2.sigsoft.org/EmpiricalStandards/docs/standards) so it can be directly proposed as a supplement or new standard. Where the guide in Section 4 conveys the *reasoning*, this standard provides the *minimum requirements* that authors, reviewers, and editors can verify.

**Design principles:**
- Follows the exact structure of existing ACM Empirical Standards: Application, Specific Attributes (Essential / Desirable / Extraordinary), General Quality Criteria, Examples of Acceptable Deviations, Antipatterns, Invalid Criticisms, Suggested Readings, and Exemplars.
- Uses bullet-point lists (not tables) to match the ACM format.
- Uses EITHER...OR constructions where multiple valid approaches exist.
- Cross-cuts existing standards (Repository Mining, Data Science, Longitudinal, Experiments)---applicable as a supplement whenever a study makes causal claims.
- Self-contained: a reviewer can use this standard without reading the rest of the paper.

**Draft structure:**

### Application

This standard applies to empirical SE studies that meet the following conditions:

- Investigates a causal research question (i.e., whether an intervention, practice, tool, or design decision affects an outcome)
- Uses observational data (not a randomized controlled experiment) to draw causal conclusions
- Employs an identification strategy to argue that the estimate has a causal interpretation

This standard does not apply to purely descriptive or predictive studies, randomized controlled experiments (see the **Experiments Standard**), or studies that explicitly disclaim any causal intent. If the study uses observational data and makes causal claims (even implicitly), this standard applies in addition to any method-specific standard (e.g., **Repository Mining**, **Data Science**, **Longitudinal**).

### Specific Attributes

#### Essential Attributes

- explicitly states a causal research question (not merely correlational or predictive)
- articulates the target trial: describes the hypothetical experiment the observational analysis attempts to emulate, specifying treatment, population, outcome, and timing
- defines the causal estimand (e.g., ATE, ATT, LATE) using potential outcomes notation or an equivalent plain-language definition
- names the identification strategy used (e.g., selection-on-observables, difference-in-differences, instrumental variables, regression discontinuity, panel fixed effects)
- states the formal identifying assumptions required for the strategy (e.g., conditional ignorability, parallel trends, exclusion restriction, strict exogeneity)
- EITHER: justifies covariate selection using a causal model (e.g., back-door criterion applied to a DAG) OR: provides a substantive argument for why each included covariate blocks a confounding path and each excluded covariate is not a confounder
- discusses which confounders the design absorbs and which remain as potential threats
- for selection-on-observables: conducts sensitivity analysis quantifying vulnerability to unmeasured confounding (e.g., Rosenbaum bounds, E-value, robustness value, coefficient stability)
- for DiD: tests and reports pre-treatment trends
- for IV: reports first-stage strength (e.g., F-statistic) and argues exclusion restriction plausibility
- for RDD: argues continuity at the threshold; reports density test (e.g., McCrary) or equivalent
- limitations are not merely listed but *mitigated* with quantitative tools (e.g., sensitivity analysis, robustness checks, falsification tests)
- at least one plausible alternative explanation is considered and addressed with evidence or argument
- discusses measurement validity: whether proxies adequately capture the constructs of interest
- causal conclusions are appropriately qualified given the strength of the identification strategy
- reports effect sizes, not just statistical significance
- distinguishes clearly between causal and associational claims in its language

#### Desirable Attributes

- presents a causal DAG (or equivalent causal model) encoding the assumed data-generating process
- discusses whether the treatment is well-defined or acknowledges compound treatment ambiguity
- discusses SUTVA (no interference between units) or justifies why interference is negligible
- discusses the internal--external validity trade-off: how the identification strategy constrains generalizability
- conducts robustness checks under alternative specifications (e.g., different control sets, functional forms, sample restrictions)
- conducts falsification or placebo tests (e.g., testing for effects on outcomes the treatment should not affect)
- discusses the direction and likely magnitude of remaining bias
- provides data and code for reproduction
- for design-based methods: discusses the extent to which the quasi-experimental variation approximates random assignment

#### Extraordinary Attributes

- triangulates across multiple identification strategies (e.g., both selection-on-observables and design-based) on the same question
- conducts formal sensitivity analysis using multiple methods (e.g., both Rosenbaum bounds and robustness values)
- pre-registers the identification strategy and analysis plan

### General Quality Criteria

Internal validity (strength of causal identification), construct validity (quality of treatment and outcome measurement), transparency of assumptions, and appropriate qualification of conclusions. External validity is important but should not override internal validity for causal claims.

### Examples of Acceptable Deviations

- A DAG is not presented if the identification strategy is design-based (e.g., DiD, RDD) and the design-specific assumptions are argued substantively, though a DAG is still desirable.
- Formal sensitivity analysis is not conducted if the study honestly qualifies its conclusions as associational or "consistent with a causal interpretation under stated assumptions" rather than claiming definitive causation.
- A formally defined estimand (ATE, ATT, LATE) is not provided if the study clearly describes in plain language what causal quantity is being targeted and for what population.
- Pre-treatment trend tests are not reported for DiD if the treatment is a one-time event with only one pre-treatment period, provided the limitation is acknowledged.

### Antipatterns

- Interpreting regression coefficients as causal effects without stating identifying assumptions ("the Table 2 fallacy")
- Including covariates without causal justification; "throwing in everything available" increases the risk of conditioning on mediators, colliders, or their descendants
- Claiming to "control for confounders" using regression without arguing that all important confounders are measured
- Acknowledging that "correlation does not imply causation" in the limitations section but writing the discussion and implications as if the findings are causal
- Using causal language ("X affects Y," "X leads to Y," "the impact of X on Y") while disclaiming any causal intent---the mismatch between language and method misleads readers
- Listing threats to validity without engaging with their severity, direction of bias, or mitigation
- Conducting sensitivity analysis but only reporting it when results are robust, suppressing cases where conclusions are fragile

### Invalid Criticisms

- The study does not use a randomized controlled experiment. The whole point of causal inference methods for observational data is to draw credible causal conclusions when randomization is infeasible.
- The study does not measure all possible confounders. No observational study can measure all confounders; what matters is whether the identification strategy and sensitivity analysis provide a credible argument.
- The study "only" estimates a local effect (LATE, effect at the threshold). Local effects are valid causal estimates; criticizing externalizability is appropriate but rejecting on this basis alone is not.
- The study's causal conclusions are "too cautious" or "too hedged." Appropriate qualification of causal claims is a strength, not a weakness.
- The effect size is small. Small effects can be practically important at scale (e.g., a small reduction in defect rates across millions of projects) and are not grounds for rejection if precisely estimated.
- The study uses an "old" or "simple" method (e.g., DiD instead of a newer estimator). What matters is whether the method's assumptions are credible in the specific context, not whether a more complex method exists.

### Suggested Readings

*(To be populated from the paper's reference list, including: Angrist & Pischke 2009, Cunningham 2021, Hernan & Robins 2020, Pearl 2009, Rosenbaum 2002, Lundberg et al. 2021, Cinelli & Hazlett 2020, Roth et al. 2023, Imbens 2020, and the SE-specific tutorials cited in Section 2.)*

### Exemplars

*(To be populated with SE papers that satisfy this standard, drawn from the paper's citation analysis and worked examples. Candidates include: Cheng et al. 2022 (panel FE at Google), Fang et al. 2022 (DiD on OSS promotion), Chen et al. 2026 (DiD on core contributor disengagement), He et al. 2026 (DiD on LLM agent adoption), Graf et al. 2024 (IV tutorial), Furia et al. 2024 (structural causal models on PL data).)*

---

## Relationship to Worked Examples (Sections 5--6)

The guide in Section 4 is self-contained and domain-neutral. The worked examples revisit and reinforce the guide's points:

- **Example A (Ray et al. -> Panel FE):** Demonstrates the guide in action: articulate the causal question (target trial, DAG) -> identify the quasi-experimental variation (panel structure) -> choose Path B (panel FE) -> probe credibility (strict exogeneity, time-varying confounders). Explicitly references the guide's subsections to show how the reasoning maps to the structure.
- **Example B (Bogner & Merkel -> DiD):** Demonstrates the guide with a different identification strategy: articulate the causal question -> reformulate the treatment (creative act emphasized in 4.2.3) -> identify staggered adoption -> choose Path B (DiD) -> probe credibility (parallel trends).

Both examples primarily demonstrate Path B (design-based identification), appropriate given the paper's emphasis on the credibility revolution. Both also use DAGs (Path A's primary tool) for reasoning about mechanisms and remaining threats, illustrating the complementary relationship.

The worked examples should explicitly call back to the guide: "As the guide in Section 4 recommends, we begin by articulating the target trial..." This reinforces the guide's applicability while showing that real applications require judgment and creativity beyond any checklist.

---

## Actionable Tasks

- [x] Revise and relocate "Choosing Among Methods," "Internal--External Validity," and current 4.1 into Section 3.4 with a clear narrative arc (see Section 3 merge description above)
- [x] Draft 4.1 "Start with the Causal Question" with domain-neutral SE vignettes
- [x] Draft 4.2.1 "Path A: DAG-Based Identification"
- [x] Draft 4.2.2 "Path B: Design-Based Identification" with data-feature-to-method table
- [x] Draft 4.2.3 "When Neither Path Is Clean"
- [x] Draft 4.3 "Probing Credibility: Limitations and Alternatives"
- [x] Draft appendix as a full ACM Empirical Standard for Causal Inquiry (Application, Specific Attributes, Quality Criteria, Acceptable Deviations, Antipatterns, Invalid Criticisms, Suggested Readings, Exemplars)
- [x] Update cross-references in Sections 5--6 to reference the guide's subsections instead of "Step 1" / "Step 2"
- [x] Update abstract and introduction: replace "four-step framework" with "guide" language
- [x] Update README.md paper vision and task backlog to reflect the revised framing
