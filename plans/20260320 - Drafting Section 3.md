## Detailed Plan for Section 3: A Primer on Causal Inference for SE Researchers

### Design Principles

Section 2 already covers the *history* of causal inference traditions and the *state of practice* in SE. Section 3 must therefore avoid rehashing history and instead deliver the *conceptual and technical toolkit* that SE researchers need to understand, assess, and conduct causal research. The current draft of Section 3 (in `main.tex`) contains substantial material but has two problems:

1. **Overlap with Section 2.** The current Section 3.1 ("What is Causality, Actually?") recounts the same historical progression (Neyman, Fisher, Rubin, Pearl, credibility revolution, modern advances) already covered in Section 2.2.1. This must be replaced with a *conceptual* treatment of what causality *means* across traditions, not when each tradition emerged.
2. **Missing narrative arc.** The current subsections (correlation != causation, regression, PO, DAGs, methods, validity) read as a textbook checklist rather than a story with a through-line. The new structure should follow a clear pedagogical arc: *what is causality?* -> *why is it hard to establish?* -> *what tools exist?* -> *which stance should SE researchers adopt?*

### Proposed Structure

#### Opening Paragraph (no subsection number)

**Purpose:** Position Section 3 relative to Section 2 and set scope.

**Content:**
- Transition from Section 2: Section 2 documented (a) the historical development of the causal inference toolkit, (b) the methodological reform in psychology and epidemiology, and (c) the quantitative gap between causal ambition and method in SE. This section now equips the reader with the conceptual and technical foundations needed to close that gap.
- Scope declaration: We cover the three conceptual pillars most relevant to empirical SE research---potential outcomes / counterfactual reasoning, graphical causal models (DAGs), and design-based identification. We do *not* cover causal discovery algorithms (learning graph structure from data), ML-based heterogeneous treatment effect estimation (causal forests, double ML), or formal verification of causal claims. Provide references for each excluded topic so interested readers know where to go.
- Justify the scope from the SE perspective: The three pillars we cover address the field's most pressing methodological gap---substantiating causal claims from observational repository data---whereas the excluded topics either require experimental data SE rarely has (heterogeneous effects) or address different questions (causal discovery, formal methods). The combination of potential outcomes + DAGs + design-based identification is what the credibility revolution in economics brought to social science; SE is the natural next audience.

#### 3.1 What Does It Mean for X to Cause Y?

**Purpose:** Give the reader an intuitive, philosophically grounded understanding of what causality *is*, told as an engaging story rather than a history lesson. This replaces the current Section 3.1 and must *not* duplicate Section 2.2.

**Narrative arc:**
1. **Start with an SE question the reader cares about.** "Does adopting TypeScript reduce defects?" Frame this as a question about what *would happen* if a team adopted TypeScript vs. what *would happen* if it did not---i.e., a question about a contrast between two worlds.
2. **The regularity / associational view (Hume).** The simplest notion: X causes Y if X is regularly followed by Y. In SE terms: if teams using TypeScript consistently have fewer bugs, we might say TypeScript "causes" fewer bugs. Immediately show why this fails---the ice cream and drowning example, or better, an SE-specific one (e.g., projects using CI/CD have fewer bugs, but that may reflect team maturity, not CI/CD itself).
3. **The counterfactual view (Lewis, Hume's second definition, Rubin).** X causes Y if Y would not have occurred had X not occurred. This is the potential outcomes idea in natural language: What would have happened to *this team* if they had *not* adopted TypeScript? The fundamental problem: We can never observe both worlds for the same unit. This is profound and non-obvious to an SE audience accustomed to thinking in terms of A/B tests or simple comparisons.
4. **The manipulationist / interventionist view (Woodward, Pearl).** X causes Y if intervening on X (holding everything else fixed) changes Y. Pearl's do-operator formalizes this: P(Y | do(X=1)) vs. P(Y | X=1). The key insight is the difference between *seeing* X=1 (conditioning) and *making* X=1 (intervening). Use the SE example: Observing that TypeScript projects have fewer bugs (conditioning) is different from forcing a team to switch to TypeScript (intervening). The former includes selection effects; the latter isolates the causal effect.
5. **The "target trial" view (Hernan).** For applied researchers, the most pragmatic formulation: Every causal question implicitly describes a hypothetical randomized experiment. Hernan's target trial framework asks: What RCT would you *ideally* run? Even though you cannot run it, articulating it clarifies the treatment, the population, the outcome, and the threats to validity. For SE: The target trial for the TypeScript question would randomly assign half of a set of JavaScript teams to adopt TypeScript and compare defect rates. Articulating this target trial immediately reveals problems---you cannot randomly assign languages, teams that would comply differ from those that would not, the "treatment" is fuzzy (full adoption? gradual migration?).
6. **Synthesis.** These perspectives are not competing theories; they are complementary lenses that modern applied research uses together. The counterfactual view gives us *estimands* (what we want to estimate). The interventionist view gives us *identification* (under what conditions can observational data approximate an intervention). The target trial view gives us *research design* (what ideal experiment are we trying to emulate). Together, they form the conceptual backbone of the rest of this primer.

**Tone:** Conversational, engaging, with concrete SE examples at every step. Minimal formalism---save equations for Section 3.3. Use rhetorical questions to motivate transitions.

**Key references:** Hume (1748) for regularity, Lewis (1973) for counterfactuals, Woodward (2003) for interventionism, Holland (1986) for "the fundamental problem," Hernan & Robins (2020) for the target trial framework.

#### 3.2 Why Naive Approaches Fail

**Purpose:** Establish *why* causal inference is hard, building on the intuition from 3.1. This section consolidates and retains the core content from the current Sections 3.2 ("Why Correlation Does Not Imply Causation") and 3.3 ("Why Multivariate Regression Usually Does Not Suffice").

**Content to keep (from current draft):**
- The three mechanisms generating spurious correlations: confounding, reverse causality, selection bias. Keep the PL-specific examples (developer expertise as confounder, teams switching to "rigorous" languages as reverse causality, conditioning on popular projects as collider bias).
- The decomposition of the observed association into causal effect + selection bias (Equation 1 in current draft).
- Why multivariate regression does not solve the problem: omitted variable bias (with the formula showing bias from unobserved confounders), bad controls (mediator bias and collider bias with PL examples).
- When regression *can* support causal claims: conditional ignorability, overlap, correct functional form.

**Content to add:**
- A brief forward pointer: Note that DAG-informed regression (using the back-door criterion to select covariates) can turn regression into a valid identification strategy *if* the DAG is correct and all required covariates are observed---but this is a big "if" in SE settings where key confounders (developer skill, team culture) are typically unmeasured. Point the reader to Section 3.3 for the full treatment of DAGs and to Section 3.4 for the pragmatic recommendation.
- A brief mention of the estimand-first principle: Before worrying about *how* to estimate, define *what* you want to estimate. The current draft jumps from "regression is bad" to "here is the PO framework" without motivating why we need to think about estimands first. A sentence or two bridging this gap would improve flow.

**Content to trim:**
- The current drafts of 3.2 and 3.3 are already fairly tight. Ensure no redundancy with the confounding discussion in 3.1 (which should be intuitive, not formula-based).

#### 3.3 The Causal Inference Toolkit: Three Pillars

**Purpose:** Introduce the three conceptual pillars---potential outcomes, DAGs, and design-based identification---at a level that gives the reader both intuition and enough technical detail to follow Sections 4--6. Each pillar gets a dedicated sub-subsection.

**Overall framing paragraph:** Note that applied causal inference rests on three complementary tools, each answering a different question:
- **Potential outcomes** answer: *What do we want to estimate?* (Estimands: ATE, ATT, LATE, CATE.)
- **DAGs** answer: *What must we assume about the world for our estimate to be valid?* (Causal structure, adjustment sets, identification.)
- **Design-based identification** answers: *How can we exploit features of the research setting to make those assumptions credible?* (DiD, IV, RDD, panel FE, synthetic control.)

Modern applied researchers use all three together: Potential outcomes define the target, DAGs encode the assumed causal structure, and design-based methods exploit quasi-random variation to achieve identification without relying on the (often untenable) assumption that all confounders are observed.

##### 3.3.1 The Potential Outcomes Framework

Retain the core content from the current Section 3.4 ("The Potential Outcomes Framework"):
- Notation and setup: $Y_i(1)$, $Y_i(0)$, the fundamental problem of causal inference.
- Causal estimands: ATE, ATT, LATE, CATE. Interpret each in SE terms ("The ATE answers: On average across all teams, how much does adopting TypeScript change defect rates?").
- The selection bias decomposition (Equation 4 in current draft) --- this is critical and well-done.
- RCTs as the gold standard: Randomization makes $(Y(1), Y(0)) \perp D$, so selection bias vanishes. SUTVA.
- Conditional ignorability and its limitations (bridge to DAGs and design-based methods).

Add emphasis on the *estimand-first* principle (Lundberg et al. 2021): Before choosing a method, define the estimand. Different estimands answer different questions, and an SE researcher must decide whether they care about the ATE (average effect across all projects) or the ATT (effect on projects that actually adopted the treatment) or the LATE (effect on projects whose adoption was driven by a specific instrument).

##### 3.3.2 Graphical Causal Models and DAGs

Retain the core content from the current Section 3.5 ("Graphical Causal Models and DAGs"):
- What a DAG is: nodes (variables), directed edges (direct causal effects), every arrow is a substantive claim.
- The PL-defect DAG (Figure 2 in current draft) --- keep this, it is effective.
- Causal paths vs. back-door paths.
- The back-door criterion and the do-calculus adjustment formula.
- Connecting DAGs to potential outcomes: When Z satisfies the back-door criterion, conditional ignorability holds.
- Alternative explanations as alternative DAGs.

Add:
- Emphasize the *transparency* value of DAGs for SE: A DAG makes every causal assumption visible and debatable. In the PL-defect debate, the unproductive back-and-forth between Ray et al. and Berger et al. could have been channeled into a productive discussion about *which edges belong in the DAG* and *which confounders are unmeasured*.
- Briefly note the limitations of DAGs: They require domain knowledge to construct (they are not learned from data in this framework); they assume no unobserved variables are omitted from the graph; and they say nothing about the *magnitude* of effects.

##### 3.3.3 Design-Based Identification

Retain the core content from the current Section 3.6 ("Overview of Identification Methods"):
- Table 2 (methods, estimands, assumptions) --- keep this, it is a valuable reference.
- The three key points: different methods estimate different quantities; design-based methods derive credibility from the research setting; quasi-experimental methods are not assumption-free.

Add:
- Brief intuitive explanation of each method with an SE example:
  - **DiD:** Compare defect trends before and after TypeScript migration in treatment projects vs. control projects. Assumption: Without migration, both groups would have followed the same trend.
  - **IV:** Find an "instrument" that affects language choice but not defects except through language. Example: A new manager who mandates TypeScript adoption. Assumption: The manager's preference affects defects *only* through the language switch.
  - **RDD:** If a policy assigns treatment based on a threshold (e.g., projects above a size threshold must adopt code review), compare projects just above and just below the threshold. Assumption: Projects near the threshold are similar in all respects except treatment.
  - **Panel FE:** Use repeated observations of the same developer or project over time, absorbing all time-invariant characteristics. Assumption: No time-varying confounders correlated with both treatment and outcome.
  - **Synthetic control:** Construct a weighted combination of untreated units to serve as a counterfactual for a single treated unit (e.g., a major framework that adopted TypeScript). Assumption: The synthetic control tracks the treated unit's counterfactual trajectory.
- Retain the internal--external validity discussion (from current Section 3.7) as a closing paragraph here, noting the hierarchy of evidence and the importance of triangulation.

#### 3.4 A Pragmatic Stance for SE Research

**Purpose:** Synthesize the three pillars into an actionable recommendation for SE researchers. This is the *opinionated* part of the primer, where we argue for a specific methodological stance rather than just surveying options.

**Core argument:**

We recommend that SE researchers adopt a pragmatic synthesis of the three pillars, drawing on the emerging consensus in applied social science (Imbens 2020, Hernan & Robins 2020, Cunningham 2021):

1. **Use potential outcomes / counterfactual reasoning / the target trial framework to reason about the *validity* of a research design.** Before analyzing data, articulate: What is the target trial? What estimand are we targeting? What would the ideal randomized experiment look like? This forces clarity about the treatment definition, the population, the outcome, and the timing---all of which are often left implicit in SE studies. The target trial framework is especially valuable because SE researchers are comfortable with the idea of controlled experiments (even if they cannot always run them); the target trial simply asks them to *describe* the experiment they wish they could run, and then evaluate how far their observational design departs from it.

2. **Use DAGs to reason about *mechanisms* and *covariate selection*.** Once the target trial is articulated, construct a DAG encoding the assumed causal structure. The DAG serves three purposes: (a) it identifies which covariates must be controlled for (back-door criterion), (b) it identifies which covariates must *not* be controlled for (mediators, colliders), and (c) it makes assumptions explicit so that reviewers and critics can challenge specific edges. For design-based methods (DiD, IV, RDD), the DAG is less central to identification---the design itself provides identification---but it remains valuable for reasoning about *which confounders the design does and does not address* and for decomposing mechanisms.

3. **Use design-based identification whenever the research setting permits.** When the data contain temporal variation (panel data), staggered adoption events (DiD), plausible instruments (IV), or assignment thresholds (RDD), exploit these features rather than relying solely on covariate adjustment. The credibility revolution's core lesson is that research design trumps statistical modeling; SE data is rich in exactly the kinds of variation that design-based methods exploit.

**Why this stance for SE specifically:**
- SE's observational data (repository mining) is plagued by *unmeasured confounders* (developer skill, team culture, organizational practices) that make selection-on-observables strategies fragile. Design-based methods sidestep this by exploiting quasi-random variation.
- SE researchers already have strong intuitions about controlled experiments from the developer study tradition (Wohlin et al.). The target trial framework bridges this intuition to observational settings.
- SE data is inherently *panel data* (repositories evolve over time, developers contribute across projects, tools are adopted in waves), making it well-suited to DiD, panel FE, and synthetic control designs that much of the social sciences lack access to.
- DAGs are a natural fit for SE because software systems are themselves structured as dependency graphs; the idea of encoding causal relationships as a graph is congenial to the SE mindset.

**Forward pointer:** This pragmatic stance is operationalized in the four-step framework (Section 4), where Step 1 constructs the DAG, Step 2 defines the estimand via potential outcomes and selects the identification strategy, Step 3 probes the assumptions, and Step 4 considers alternative DAGs.

### Relationship to Existing Content in `main.tex`

The restructuring implies the following changes to the current `main.tex` Section 3:

| Current subsection | Disposition |
|---|---|
| 3.1 "What is Causality, Actually?" | **Replace entirely.** Current content overlaps with Section 2.2.1. New 3.1 is a *conceptual* treatment of perspectives on causality (regularity, counterfactual, interventionist, target trial), not a historical narrative. |
| 3.2 "Why Correlation Does Not Imply Causation" | **Keep and consolidate** into new 3.2 ("Why Naive Approaches Fail"), merged with current 3.3. |
| 3.3 "Why Multivariate Regression Usually Does Not Suffice" | **Merge** into new 3.2. Add brief DAG-informed regression forward pointer. |
| 3.4 "The Potential Outcomes Framework" | **Move** into new 3.3.1. Add estimand-first emphasis. |
| 3.5 "Graphical Causal Models and DAGs" | **Move** into new 3.3.2. Add transparency-for-SE emphasis and DAG limitations. |
| 3.6 "Overview of Identification Methods" | **Move** into new 3.3.3. Add intuitive SE example for each method; merge internal--external validity discussion. |
| 3.7 "Internal--External Validity Trade-Off" | **Merge** as closing paragraphs of new 3.3.3. |
| *(new)* | **Add** new 3.4 ("A Pragmatic Stance for SE Research") --- entirely new content. |

---
