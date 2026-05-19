# Literature-Justified DAG Redesign for Sections 3 and 4

**Status:** Drafting

## Motivation

The DAGs currently in Section 3 (Figure `fig:ai-dag`, the pedagogical primer DAG) and Section 4 (Figure `fig:temporal-dag`, the temporal DAG for the worked example) feel structurally weak for two reasons.

1. **No theoretical anchoring.** The current draft does not stress that DAGs must be derived from prior theory and empirical knowledge, and the DAGs themselves were lifted wholesale from an earlier PL-vs-defects example: nodes were simply renamed (`PL` → `AI Tool Adoption`, `Defects` → `Dev. Velocity`, mediators `Code Style` → `Code Generation` etc.) without going back to the AI-coding-tool literature to justify each edge. The result is that the running example's most important diagram looks like it came out of the blue.
2. **Aesthetic mismatch with the thesis.** The current TikZ uses plain `draw, rounded corners` boxes with no semantic color or edge coding, while the thesis figures (`analysis-cursor.tex`, `analysis-fake-stars.tex`, `analysis-pinning.tex`) use a consistent palette to communicate node role (treatment / mediator / outcome / confounder / residual threat) and edge role (back-door blocked vs.\ identified mechanism vs.\ reverse causality vs.\ measurement).

This plan fixes both gaps in two passes: (i) write the literature-justified theoretical setup that precedes each DAG, and (ii) redraw both DAGs using the thesis style.

## Pedagogical Constraints

- **Section 3 DAG (`fig:ai-dag`)**: simple enough for first-time readers. Target exactly **one mediator, one collider, and 2--3 confounders** (one of them unobserved). Single time slice; the temporal subtlety is deferred to Section 4 as already done. Every node and edge must be traceable to a sentence in the surrounding text or footnote.
- **Section 4 DAG (`fig:temporal-dag`)**: builds on the Section 3 DAG by splitting time-varying covariates into pre- and post-treatment incarnations. Same node set + temporal duplication; do not introduce new substantive nodes.
- **Consistency**: The Section 4 DAG must visibly extend the Section 3 DAG (same colors for same roles, same node labels for nodes that carry over). A reader who understood Figure 2 should recognize Figure 6 as "the same DAG with time".

## Literature Anchors for Each Node

These are the citations the prose around each DAG must lean on. All keys already exist in `paper/references.bib`.

| Node | Role | Literature anchor |
|---|---|---|
| AI Tool Adoption ($D$) | Treatment | `DBLP:conf/msr/HeMAKV26` (project-level systematic adoption operationalized via AI config files; the treatment construct of this paper) |
| Dev. Velocity ($Y$) | Outcome | `DBLP:conf/sigsoft/ChengMCJGKZ022` (commit-based productivity at Google); proxy discussion in Section 4.1 |
| **Mediator: Code Generation Speed** | Mediator | `cui2025effects` ($+26\%$ task completion in three firm RCTs, $N{=}4{,}867$); `peng2023impact` ($-55.8\%$ task time, JS); `DBLP:conf/icse-seip/ParadisGMNMMZFC25` ($\approx-21\%$ task time at Google). This is the single best-supported mechanism in the RCT literature and the only one we keep in the pedagogical DAG. |
| **Collider: Popularity (stars/attention)** | Collider | `DBLP:conf/icse/FangLHV22` (social-media promotion $\to$ stars and contributors); informally, both AI adoption and high commit activity attract HN/Reddit/Twitter coverage in 2024--2026. This is the same node used downstream in Section 4 for the temporal-collider example. |
| Confounder: Team Skill (unobserved) | Confounder | `oster2019unobservable`, `cinelli2020making` already cited for sensitivity; the unobservable nature of developer skill is the load-bearing reason Section 4.1's $\delta^* = 0.12$ matters. |
| Confounder: Project Maturity (repo age) | Confounder | Empirical evidence is Table `tab:descriptive` (adopters are younger: 7.7 vs.\ 9.4 yr, SMD $= -0.37$). The substantive "why it confounds" story is domain knowledge (younger projects are less encumbered by entrenched workflows and are typical early adopters of new developer tools; older projects also have larger commit baselines mechanically). No prior-lit citation is needed and the closest paper we have on this question — `DBLP:conf/msr/HeMAKV26`, our own Cursor study — is already cited as the worked example's basis. |
| Confounder: Language / Domain | Confounder | Empirical evidence is Table `tab:descriptive` (heavy TypeScript skew, SMD $= 0.50$; near-zero Swift/C uptake). The substantive "why it confounds" story is again domain knowledge: AI coding tools are differentially capable across languages (better LLM training data for TS/Python than C/Swift) and languages also have different baseline velocity patterns and ecosystem conventions. Same anchoring as Project Maturity — `DBLP:conf/msr/HeMAKV26` for the worked-example link. **Do not cite `DBLP:conf/sigsoft/RayPFD14`**; that paper is about PL and code quality, not AI-tool adoption rates by language. |

Mediators *dropped* from the pedagogical DAG (kept only briefly in Section 4 text, not in any figure):
- "Workflow Automation" — currently in `fig:ai-dag`, but the evidence is qualitative/anecdotal and dilutes the pedagogical point. Mention in passing as a *secondary* mechanism in prose, not in the figure.
- "Code Review Acceleration" — Borusyak vs.\ CS divergence (Section 4.2) is already the place where mediator bias gets concretized, so the pedagogical figure does not need to multiply mediators.

Confounders *dropped*:
- "Team Size" as a separate node — folded into Team Skill in the pedagogical DAG; reinstated as its own time-varying node in the temporal DAG (where the panel actually measures it).
- "Organization" as a separate node — folded into Project Maturity in the pedagogical DAG; reinstated in the temporal DAG (already a structurally pre-treatment covariate in Table 4).

## Pedagogical DAG Sketch (Section 3.3.2)

```
                Team Skill (unobs., dashed)   Project Maturity   Domain (PL)
                       \         |          /
                        \        |         /
                         v       v        v
        AI Tool Adoption  ────────►  Code Generation  ────────►  Dev. Velocity
              │                                                       │
              │                                                       │
              └──────────────────►  Popularity (stars)  ◄──────────────┘
                                       [collider]
```

- 1 mediator: Code Generation
- 1 collider: Popularity
- 3 confounders: Team Skill (unobserved, dashed border), Project Maturity, Domain
- Footnote previewing that Popularity changes role over time, with forward reference to Section 4 — the existing footnote (currently around line 137 of `paper/2-primer.tex`) already does this and should be kept.

## Temporal DAG Sketch (Section 4.1.2)

Same backbone, but:
- Pre-treatment time-varying nodes: `Popularity_{t-1}`, `Demand_{t-1}`, `Activity_{t-1}`, `Team Size_{t-1}` (confounders)
- Post-treatment time-varying nodes: `Popularity_{t+1}`, `Demand_{t+1}`, `Activity_{t+1}`, `Team Size_{t+1}` (colliders)
- Structurally pre-treatment confounders: `Domain`, `Organization`, `Project Maturity`, `Team Skill` (Team Skill dashed = unobserved)
- Mediator: `Code Generation` (single mediator, consistent with the Section 3 figure)
- Treatment $D$, Outcome $Y$

This keeps the node count manageable while making the "split-by-time" idea visually unambiguous.

## Aesthetic Conventions (Borrowed from Thesis)

Style block to copy into both figures (with minor tuning for the pedagogical version):

```latex
\begin{tikzpicture}[
    >=latex, font=\scriptsize,
    confbox/.style={draw, rounded corners, fill=gray!12, align=left,
                    inner sep=4pt},
    tnode/.style={draw, rounded corners, fill=green!20, very thick,
                  minimum height=0.7cm, minimum width=2.6cm,
                  align=center, font=\bfseries\scriptsize},
    mnode/.style={draw, rounded corners, fill=yellow!25,
                  minimum height=0.6cm, minimum width=2.6cm, align=center},
    ynode/.style={draw, rounded corners, fill=blue!10,
                  minimum height=0.6cm, minimum width=2.6cm, align=center},
    cnode/.style={draw, rounded corners, fill=orange!15,
                  minimum height=0.6cm, minimum width=2.6cm, align=center},
    unobs/.style={draw, rounded corners, dashed, fill=gray!5,
                  minimum height=0.6cm, minimum width=2.6cm, align=center,
                  font=\itshape\scriptsize},
    cedge/.style={->, gray, dashed, semithick},
    medge/.style={->, black, semithick},
    coledge/.style={->, orange!70!black, semithick},
]
```

Edge semantics (used identically in both figures):
- **Solid black (`medge`)**: identified causal mechanism (treatment $\to$ mediator $\to$ outcome).
- **Dashed gray (`cedge`)**: back-door path through a confounder; the prose explains how the design blocks it.
- **Solid orange (`coledge`)**: edges into a collider; the prose explains why the design must *not* condition on it.
- **Dashed border (`unobs`)**: variable is unobserved in the data (Team Skill).

Caption convention (also borrowed): each caption walks through (1) the treatment $\to$ mediator $\to$ outcome causal path, (2) the confounding back-door paths and how they are blocked, (3) the collider and why it must not be conditioned on, and (4) the unobserved confounder and its sensitivity-analysis implication.

## Where the Literature Justification Lives

**Decision: main body text, not the figure caption.** The pedagogical message of Section 3 is "DAGs must be derived from theory"; burying the citations in a caption signals that the justification is figure-decoration rather than the load-bearing setup the figure rests on. Concretely:
- **Section 3**: 1--2 new body paragraphs (or expansion of the existing `\paragraph{Directed Acyclic Graphs.}` block) that walk node-by-node through the literature anchors *before* the figure appears. This models the practice we want SE readers to adopt.
- **Section 4**: a single short paragraph noting that the temporal DAG is the same theory as Figure `fig:ai-dag` with time-varying covariates split into pre- and post-treatment nodes. No need to repeat per-node citations.
- **Captions** (both figures): tight figure-description only --- paths, colors, what is dashed, what role each color codes. No citations in captions.

## Tasks

### Prose changes in Section 3 (`paper/2-primer.tex`)

- [ ] In the lead-in to Section 3.3.2 (the "Build on Prior Research" paragraph already exists at Section 3.4 / `sec:stance-prior-research`), add 1--2 sentences *before* introducing Figure `fig:ai-dag` that explicitly say: *"The DAG below is not derived from the data we are about to analyze. It encodes substantive claims drawn from prior empirical and experimental work on AI coding tools."*
- [ ] Justify the **Code Generation** mediator with one inline citation cluster: `\cite{cui2025effects, peng2023impact, DBLP:conf/icse-seip/ParadisGMNMMZFC25}`. One sentence: "Three independent randomized experiments establish that AI coding tools accelerate per-task code production, motivating Code Generation as the load-bearing mediator on the AI Tool Adoption $\to$ Dev. Velocity path."
- [ ] Justify the **Popularity** collider with `\cite{DBLP:conf/icse/FangLHV22}`. One sentence connecting that paper's social-media $\to$ stars finding to the symmetric argument that both AI adopters and high-velocity projects attract attention.
- [ ] Justify the **Team Skill** confounder (unobserved) by pointing to the descriptive imbalance table in Section 4.1 (Table `tab:descriptive`) as the post-hoc empirical signature, plus a forward reference to the Oster sensitivity result.
- [ ] Justify the **Project Maturity** and **Domain** confounders with one sentence each, framed as domain-knowledge claims about technology adoption among open-source projects and made empirically concrete by the imbalance in Table `tab:descriptive` (age SMD $-0.37$; TypeScript SMD $+0.50$). Do **not** cite Ray et al.\ 2014 or Cheng et al.\ 2022 for these — neither paper studies AI-tool adoption patterns. If a literature anchor is desired, cite our own `DBLP:conf/msr/HeMAKV26` as the worked-example basis.
- [ ] Acknowledge dropped nodes in a parenthetical: "Other mediators (workflow automation, code review acceleration) and confounders (team size, organization) are plausible but omitted from this pedagogical figure; the temporal DAG in Section 4 reintroduces the time-varying ones."

### Prose changes in Section 4 (`paper/3-worked-example.tex`)

- [ ] In Section `sec:temporal-dag`, add one paragraph that says: the temporal DAG is the *same* causal theory as Figure `fig:ai-dag`, with the time-varying covariates split into pre- and post-treatment nodes — no new substantive claims are made. This makes the connection to Section 3 explicit.
- [ ] Replace the current "Code Generation / Workflow Automation" pair of mediators with a single Code Generation node, matching the Section 3 figure. Update the surrounding text (lines around 161 of `paper/3-worked-example.tex`) accordingly.
- [ ] Keep Team Skill as the single unobserved confounder; do not introduce new latent nodes.

### Figure redraws

- [ ] **`fig:ai-dag` (Section 3)**: rewrite the TikZ block (lines 140--183 of `paper/2-primer.tex`) using the style block above. Layout: confounders on top row, treatment / mediator / outcome on the middle row, collider on the bottom. Use `confbox` to group the three confounders into one gray box (with Team Skill marked $\bullet$ \emph{Team Skill (unobserved)} so the prose can still single it out), keeping the figure compact.
- [ ] **`fig:temporal-dag` (Section 4)**: rewrite the TikZ block (lines 164--241 of `paper/3-worked-example.tex`) using the same style block. Keep the four-column time-varying layout but recolor pre-treatment nodes as confounders (gray-ish) and post-treatment nodes as colliders (orange). Drop "Workflow" so there is one mediator. Reuse the same node labels as Section 3 wherever they carry over.
- [ ] Verify both figures compile with `pdflatex` and visually inspect the resulting page in `main.pdf` (no overlapping boxes, no clipped arrows, captions still fit on a single page float).

### Captions

- [ ] Rewrite both captions following the thesis caption convention: (1) the identified path, (2) the back-door paths and how they are blocked, (3) the collider, (4) the unobserved confounder.
- [ ] Keep both captions to ${\le}5$ sentences each.

### Cross-references and consistency

- [ ] Audit every sentence in Sections 3 and 4 that names "Code Generation", "Workflow Automation", "Team Size", or "Organization" as a node, and update where the node has been removed or renamed.
- [ ] Ensure `sec:guide-path-a` (the "Use DAGs to Reason About Mechanisms" paragraph in Section 3.4) still makes sense with the simpler figure — likely no change needed, but verify.
- [ ] No changes to bibliography needed — all anchor citations already exist (`cui2025effects`, `peng2023impact`, `DBLP:conf/icse-seip/ParadisGMNMMZFC25`, `DBLP:conf/icse/FangLHV22`, `DBLP:conf/msr/HeMAKV26`, `DBLP:conf/sigsoft/ChengMCJGKZ022`, `DBLP:conf/sigsoft/RayPFD14`, `oster2019unobservable`, `cinelli2020making`).

## Out of Scope

- Adding causal-discovery-based edge proposals (Hulse et al.\ 2025 is already cited but not used to justify any specific edge — keeping the DAG strictly theory-driven for pedagogical clarity).
- Network/SUTVA-aware DAG extensions (mentioned in Section 3.4 but outside the worked example's scope).
- Revisiting the regression specification or estimator choice in Section 4.1 — the redesigned DAG should produce *exactly* the same adjustment set (all pre-treatment nodes minus mediators and colliders) as the current draft, so numerical results do not change.
