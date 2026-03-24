# Plan: Revising Section 4 --- From Primer to Practice

## Problem Statement

Section 3 delivers a dense primer spanning potential outcomes, DAGs, and design-based identification.
An SE researcher reading it for the first time may feel overwhelmed and unsure how to *apply* this material to their own work.
Section 4 must bridge the gap between conceptual foundations and practical research activity.

The current four-step framework (derive causal theory -> define estimand and assumptions -> acknowledge limitations -> navigate alternatives) is a reasonable skeleton, but three concerns motivate a revision:

1. **Prescriptiveness vs. creativity.** Causal inference is partly an art---the researcher must get creative in finding identification strategies that exploit the specific structure of their data and setting. A rigid "Step 1, 2, 3, 4" recipe may obscure this.
2. **Two fundamentally different paths.** The primer introduces two identification paradigms---selection-on-observables (DAG + back-door criterion) and design-based identification (DiD, IV, RDD, panel FE)---but the current framework does not clearly articulate when each is appropriate or how the researcher chooses between them.
3. **Structural overlap with Section 3.** The current Section 4 opens with "Choosing Among Methods" and "Internal--External Validity Trade-Off" paragraphs plus a "Pragmatic Stance" subsection (4.1) that read as the capstone of Section 3's primer rather than the start of a new framework section. The actual four steps occupy only ~2 pages.

## Design Principles for the Revised Section 4

- **Narrative function:** Section 4 is the *bridge* between "here is the toolkit" (Section 3) and "here is how we apply it" (Sections 5--6). It should feel like a trusted colleague walking the reader through the thinking process, not a bureaucratic checklist.
- **Honest about uncertainty:** Causal inference in practice is iterative. The researcher often revisits earlier decisions as they learn more about the data. The section should convey this without losing structure.
- **Two audiences:** (a) Researchers designing a new study, and (b) researchers (or reviewers) evaluating an existing study's causal claims. The framework should serve both.

---

## Key Structural Decision: What to Do with the "Pragmatic Stance" Material

The current Section 4 lines 619--667 contain three blocks that are not part of the four-step framework itself:

| Block | Lines | Content |
|---|---|---|
| "Choosing Among Methods" | 622--626 | Different methods estimate different quantities; design-based methods have transparent assumptions; DAGs remain valuable alongside design-based methods |
| "Internal--External Validity Trade-Off" | 628--633 | Hierarchy of evidence; triangulation |
| Subsection 4.1 "A Pragmatic Stance for SE Research" | 635--667 | Three recommendations (use target trial reasoning, use DAGs for mechanisms/covariates, use design-based identification when possible); why this fits SE |

**Recommendation:** Move these three blocks to the end of Section 3 (as a new 3.4 "A Pragmatic Stance for SE Research"), since they synthesize the primer content rather than introduce a new framework.
This is consistent with the Section 3 plan in `20260320 - Drafting Section 3.md`, which already proposed a 3.4 with exactly this content.
Section 4 then opens cleanly with the framework itself, without preamble that belongs in the primer.

- [ ] Relocate "Choosing Among Methods," "Internal--External Validity," and current 4.1 into Section 3.4

---

## The Core Question: How to Frame the Framework

Below are three options for the overall framing of Section 4, with pros and cons. We recommend **Option B** but present all three for discussion.

### Option A: Keep the Four Steps As-Is (Minor Polish)

Retain the current Step 1 -> 2 -> 3 -> 4 structure with light editorial revision.

**Pros:**
- Simple, memorable, easy to reference in the worked examples.
- Already drafted; minimal rewriting.
- Works well as a diagnostic tool for evaluating published studies.

**Cons:**
- Reads as prescriptive; does not convey the creative, context-dependent nature of causal inquiry.
- Steps 1 and 2 conflate two very different research workflows (DAG-based identification vs. design-based identification) into a single linear sequence.
- Risks the reader treating it as a bureaucratic checklist ("I did the four steps, so my study is causal").

### Option B: Reframe as a Decision-Guided Workflow with Branching Paths (Recommended)

Replace the four numbered steps with a workflow that branches based on the researcher's setting. The section is structured around a central decision: *What identification strategy does your data and setting support?*

**Structure:**

> **Section 4: Conducting Credible Causal Inquiry in SE**
>
> 4.1 Start with the Causal Question (universal)
> 4.2 Two Paths to Identification
>   - Path A: DAG-Based Identification (selection-on-observables)
>   - Path B: Design-Based Identification (quasi-experimental)
> 4.3 Probing Credibility: Limitations and Alternatives (universal)
> 4.4 Guidance: Choosing Your Path

See detailed content below.

**Pros:**
- Makes the fundamental choice (DAG-based vs. design-based) explicit and central.
- Naturally conveys that causal inference requires creativity---the researcher must assess their specific data structure to find the right path.
- The branching structure honestly reflects that there is no single recipe.
- Still provides concrete, actionable guidance (not vague).
- The two worked examples naturally demonstrate one path each (Example A -> panel FE / design-based; Example B -> DiD / design-based; and the DAG analysis in both serves the DAG-based path too).

**Cons:**
- More complex structure than the current four steps.
- Requires more writing.
- The "two paths" framing is somewhat simplified---in practice, researchers often combine elements of both.

### Option C: Remove the Framework Entirely; Use Narrative Guidance

Replace the framework with a discursive section that walks through the *reasoning process* of a causal inquiry via extended examples, without enumerating steps or paths. The section reads as "here is how an experienced causal researcher thinks about an SE problem."

**Pros:**
- Most honestly conveys the artful, context-dependent nature of causal inference.
- Avoids the risk of the reader treating any framework as a mechanical checklist.

**Cons:**
- Loses the structural anchor that the worked examples reference ("Step 1 of the framework").
- Harder for a novice reader to extract actionable guidance.
- A tutorial paper benefits from concrete, referenceable structure.
- The diagnostic use case (evaluating published work) is harder without explicit criteria.

---

## Detailed Content Plan for Option B (Recommended)

### 4.1 Start with the Causal Question

**Purpose:** The universal first move in any causal inquiry---articulate the question with precision.

**Content:**
- **Articulate the target trial.** Before touching data, describe the hypothetical randomized experiment you wish you could run. This forces clarity on: What is the treatment? What is the population? What is the outcome? What is the timing? (Retain the target trial material from the current 4.1, but framed as the *first* move rather than as a standalone recommendation.)
- **Define the estimand.** Using the potential outcomes language from Section 3, state the causal quantity of interest (ATE, ATT, LATE). Emphasize that this is a *substantive* decision, not a statistical one.
  - Absorb the current Step 2 "estimand-first" material here.
- **Construct a preliminary DAG.** Even before choosing an identification strategy, sketch a DAG encoding the researcher's beliefs about the causal structure. This DAG will be refined in subsequent steps, but it immediately (a) surfaces confounders, mediators, and colliders, (b) reveals whether the treatment is well-defined or compound, and (c) makes assumptions visible for critique.
  - Absorb the current Step 1 material here.
- **Illustrate** with the PL--defect question: target trial = randomly assign teams to TypeScript; estimand = ATE of TypeScript adoption on defect density; preliminary DAG = Figure 2 from Section 3.

**Tone:** This step is *always* the right starting point, regardless of what comes next. It is the non-negotiable foundation.

**Key message:** *Before you analyze, define what you are asking and what you are assuming about the world.*

### 4.2 Two Paths to Identification

**Purpose:** The central creative act---finding an identification strategy that is credible given the data and setting. This is where the researcher must get creative, and where causal inference becomes an art.

**Opening framing paragraph:**
- The preliminary DAG from 4.1 reveals the confounders and mechanisms. The researcher now faces the key strategic question: *How will I argue that my estimate has a causal interpretation?*
- Two broad families of strategies exist, and the choice depends on the data structure and the plausibility of the required assumptions.
- In some settings, one path is clearly superior; in others, the researcher may combine elements of both or triangulate across them.
- Emphasize: there is no algorithm for this choice. The researcher must assess the specific features of their data and setting. This is where domain expertise and methodological creativity intersect.

#### Path A: DAG-Based Identification (Selection-on-Observables)

**When to use:** The researcher believes they can measure all important confounders identified in the DAG from 4.1, or at least argue persuasively that unmeasured confounders are negligible.

**Content:**
- Apply the back-door criterion to the DAG to identify the sufficient adjustment set.
- Choose an estimation method (regression, matching, IPW, doubly robust).
- Justify covariate selection explicitly using the DAG (not by "throwing in everything available").
- Conduct sensitivity analysis to probe vulnerability to unmeasured confounding (Rosenbaum bounds, E-values, robustness values, coefficient stability).

**Honest caveat:** In many SE settings, key confounders (developer skill, team culture, organizational practices) are unmeasurable from repository data. When the DAG reveals important unmeasured confounders, selection-on-observables is fragile and the researcher should consider Path B or acknowledge the limitation prominently.

**SE-specific guidance:**
- DAG-based identification works best when rich survey or organizational data is available (not just repository mining).
- Even with repository data, DAGs remain valuable for *justifying* which variables to include and exclude, even if full identification is not achieved.

#### Path B: Design-Based Identification (Quasi-Experimental)

**When to use:** The data contain features that provide quasi-random variation in treatment assignment---temporal variation (panel data), staggered adoption (DiD), plausible instruments (IV), or assignment thresholds (RDD).

**Content:**
- Identify the quasi-experimental variation: What feature of the setting provides as-if-random variation?
- Match the variation to a method: panel structure -> panel FE; staggered adoption -> DiD; external shock -> IV; threshold assignment -> RDD.
- State the method-specific assumptions (parallel trends, exclusion restriction, continuity at threshold, strict exogeneity) and argue for their plausibility using domain knowledge and the DAG from 4.1.
- Where possible, conduct partial tests of the assumptions (pre-trend tests for DiD, first-stage F-test for IV, McCrary density test for RDD).

**Honest caveat:** Design-based methods are not assumption-free. They replace the untestable "all confounders measured" with different assumptions (parallel trends, exclusion restrictions) that must be argued substantively. The DAG from 4.1 helps clarify which confounders the design absorbs and which remain as threats.

**SE-specific guidance:**
- SE data is *rich* in the temporal and structural variation that design-based methods exploit: repositories evolve over time, developers contribute across projects, tools are adopted in waves, platform policies create natural experiments.
- Point to specific SE data features and the methods they support. Consider including a small table or decision aid:

| Data Feature | Suggested Method | Example |
|---|---|---|
| Same units observed over time | Panel FE | Developer writing in multiple languages |
| Staggered adoption events | DiD | Projects migrating to TypeScript at different times |
| External shock affecting treatment | IV | Manager mandate, platform policy change |
| Threshold-based assignment | RDD | Eligibility based on project size / contributor count |

#### Subsubsection or Callout: When Neither Path Is Clean

**Purpose:** Honest acknowledgment that many SE settings do not neatly fit either path.

**Content:**
- Sometimes the DAG reveals unmeasured confounders *and* no quasi-experimental variation is available. In these cases, the researcher should:
  - Use the best available strategy (often DAG-based with careful sensitivity analysis).
  - Be transparent about the limitations.
  - Frame conclusions as "consistent with a causal interpretation under assumptions X, Y, Z" rather than as definitive causal claims.
  - Consider whether the research question can be *reformulated* to exploit available variation (this is the creative act---e.g., Example B reformulates "language effect" as "type system adoption" to enable a DiD design).
- Triangulation: Multiple imperfect approaches that converge on the same conclusion provide stronger evidence than any single approach.
- The pragmatic bottom line: *An honest, well-argued correlational analysis that explicitly states its identification limitations is more valuable than a spurious claim of causation.*

### 4.3 Probing Credibility: Limitations and Alternatives

**Purpose:** After choosing an identification strategy, the researcher must honestly assess its fragility. This section absorbs the current Steps 3 and 4.

**Content (from current Step 3 --- Limitations):**
- No study achieves perfect identification. Limitations should be *mitigated*, not merely listed.
- Sensitivity analysis tools: Rosenbaum bounds, coefficient stability (Oster), robustness values (Cinelli & Hazlett), pre-trend tests (for DiD), over-identification tests (for IV).
- Measurement challenges specific to SE: noisy proxies (bug-fix commits for defect proneness), construct validity issues, SUTVA violations in interconnected software ecosystems.

**Content (from current Step 4 --- Alternative Explanations):**
- Consider rival causal structures (alternative DAGs) that could generate the same observed patterns.
- Derive testable implications that discriminate among alternatives.
- The goal is not to eliminate all alternatives but to engage transparently with the most plausible ones.
- Retain the three illustrative challenges from the current Step 4 (alternative mechanism, unmeasured confounding, reverse causality).

**Tone:** This is where the researcher demonstrates intellectual honesty. The mark of a credible causal study is not the absence of limitations but the transparency with which they are addressed.

### 4.4 Guidance: Choosing Your Path

**Purpose:** Practical guidance for the researcher facing a new problem. This is the "art" subsection.

**Option for this subsection (choose one):**

- [ ] **Option B1: Decision flowchart.** A visual flowchart (TikZ figure) guiding the researcher through the key questions: Do you have panel data? -> Consider panel FE. Is there a staggered adoption event? -> Consider DiD. Can you measure all confounders? -> Consider DAG-based. None of the above? -> Honest correlational analysis with sensitivity analysis.
  - *Pro:* Concrete, actionable, visually memorable.
  - *Con:* May feel too prescriptive; real decisions are messier than a flowchart.

- [ ] **Option B2: Narrative guidance with worked micro-examples.** Instead of a flowchart, provide 3--4 short vignettes (1 paragraph each) showing how a researcher in different SE settings would reason about their identification strategy.
  - *Pro:* Conveys the creative, context-dependent nature of the decision.
  - *Con:* Less structured; harder to reference quickly.

- [ ] **Option B3: Both.** Flowchart as the primary reference, with a short paragraph for each branch illustrating the reasoning.
  - *Pro:* Best of both worlds.
  - *Con:* May be too long.

---

## Relationship to Worked Examples (Sections 5--6)

The revised Section 4 should be *referenced* by the worked examples, not *repeated* in them. Currently, each worked example "walks through all four steps." Under the revised structure:

- **Example A (Ray et al. -> Panel FE):** Demonstrates the workflow: articulate the causal question (target trial, DAG) -> identify the quasi-experimental variation (panel structure in GitHub data with developers writing in multiple languages) -> choose Path B (panel FE) -> probe credibility (strict exogeneity, time-varying confounders).
- **Example B (Bogner & Merkel -> DiD):** Demonstrates the workflow: articulate the causal question (target trial, DAG) -> reformulate the treatment (from "language" to "type system adoption") -> identify the quasi-experimental variation (staggered TypeScript migration events) -> choose Path B (DiD) -> probe credibility (parallel trends, anticipation).

Both examples primarily demonstrate Path B (design-based identification), which is appropriate given the paper's emphasis on the credibility revolution and the weakness of selection-on-observables in SE settings. However, both also use DAGs (Path A's primary tool) for reasoning about mechanisms and remaining threats, illustrating the complementary relationship between the two paths.

**Note:** If we want to demonstrate Path A (DAG-based identification), we could add a brief callout or sidebar in one of the worked examples showing what a DAG-based analysis would look like and why it is less credible in that specific setting (because key confounders are unmeasured). This reinforces the paper's argument for design-based methods without dismissing DAG-based identification entirely.

---

## Section Title Options

The current title "A Pragmatic Stance of Causal Inference in Empirical SE Research" is vague and overlaps with the Section 3 capstone. Possible alternatives:

- [ ] **"Conducting Credible Causal Inquiry in SE"** --- emphasizes the practical activity, not the abstract stance.
- [ ] **"From Question to Identification: A Workflow for Causal SE Research"** --- emphasizes the process.
- [ ] **"A Framework for Assessing and Designing Causal Studies in SE"** --- retains "framework" language, emphasizes dual diagnostic/constructive purpose.
- [ ] **"The Causal Research Workflow"** --- short and direct.

---

## Checklist / Actionable Tasks

After the above decisions are made:

- [ ] Relocate "Choosing Among Methods," "Internal--External Validity," and current 4.1 "Pragmatic Stance" to Section 3.4
- [ ] Draft 4.1 "Start with the Causal Question" (absorbing current Steps 1 and 2's estimand material)
- [ ] Draft 4.2 "Two Paths to Identification" with Path A and Path B subsections
- [ ] Draft the "When Neither Path Is Clean" callout
- [ ] Draft 4.3 "Probing Credibility" (absorbing current Steps 3 and 4)
- [ ] Draft 4.4 "Guidance: Choosing Your Path" (decision flowchart or narrative)
- [ ] Decide on section title
- [ ] Update cross-references in Sections 5--6 (replace "Step 1" / "Step 2" references with the new structure)
- [ ] Update README.md task backlog to reflect the revised plan
- [ ] Update abstract and introduction to reflect the revised framing (if the four-step language changes)

---

## Open Questions

1. **Should the section explicitly use the word "framework"?** The word conveys structure and referencability, but it also implies a fixed recipe. Alternative: "workflow," "approach," "guide."

2. **How much SE-specific guidance belongs here vs. in the worked examples?** The decision table (data feature -> method) is helpful but may be better placed in a discussion section where it can draw on the worked examples as evidence.

3. **Should we include a one-page "cheat sheet" or summary table?** A condensed reference (question to ask at each stage, common pitfalls, tools) could be valuable for practitioners. This could go at the end of Section 4 or in an appendix.

4. **How to handle the diagnostic vs. constructive duality?** The current framework serves both as a tool for evaluating existing studies and for designing new ones. The revised structure should preserve this duality---the branching paths work for both (a reviewer asks "what identification strategy did the authors use?" just as a designer asks "what identification strategy should I use?").
