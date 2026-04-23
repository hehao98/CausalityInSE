# Reframing the Worked Example as a Triangulation Story

**Created:** 2026-04-23
**Last updated:** 2026-04-23 (literature sweep completed)
**Status:** Draft — literature sweep in, revision writing pending

## Motivation

The worked example currently argues **"design > estimator"**: each methodological
step (kitchen-sink → DAG-justified OLS → PSM/IPW → ITS → DiD) shrinks the
estimate, and the shrinkage is driven by the research design, not the
statistical machinery. This is the *methodological* payoff.

A common defense of naive estimates in applied work---especially in
economics---is that "we care about the direction, not the magnitude." Under
that frame, shrinking $+911\%$ to $+32\%$ is intellectually interesting but
substantively unimportant: the sign is the same either way.

**That defense fails here, and the failure is the story.** Two observations
make our worked example unusually compelling:

1. **The naive estimate encodes the AI hype narrative.** $+911\%$ (or even
   $+158\%$) would, if taken at face value, confirm the strongest industry
   claims that AI coding tools produce transformational, order-of-magnitude
   productivity gains. No published field experiment supports anything near
   that magnitude.
2. **The design-based estimate is consistent with controlled evidence.** The
   $+32\%$ to $+52\%$ ATT sits just above the best multi-firm RCT anchor
   (Cui et al.\ 2025 at $+26\%$, SE $\approx 10\%$) and within the broader
   range established by controlled experiments. The naive estimate is
   inconsistent with every RCT on record by roughly an order of magnitude.

So the worked example is doing two things at once:

- **Methodological:** showing that design choices drive estimate magnitude.
- **Substantive:** showing that the design-based estimate triangulates with
  external experimental evidence, while the naive estimate is internally
  inflated by exactly the selection and trend biases the toolkit is built
  to remove.

The current draft under-sells the second half. The plan below adds a
triangulation layer to the worked example's takeaway without disturbing the
core methodological argument.

## Literature sweep: verified evidence

Completed 2026-04-23. Every study below was verified against a primary
source (arXiv PDF, NBER/SSRN landing, publisher DOI, or official report).
See the sweep output for per-study URLs and caveats.

### Triangulation anchors (RCT / field experiment)

| Study | Design | N | Outcome | Effect | Construct vs. ours |
|---|---|---|---|---|---|
| Peng et al.\ (2023), arXiv 2302.06590 | Lab RCT, one JS task | 95 freelance devs | Time-to-complete | **−55.8% time** (faster) | Per-task time, not output volume |
| Paradis et al.\ (2025), ICSE-SEIP | Enterprise RCT at Google | 96 SWEs | Time on enterprise task | **≈ −21% time**, wide CI | Per-task time |
| Cui et al.\ (2025), NBER WP 33777 / Management Science | Three pooled firm RCTs | 4,867 devs (Microsoft, Accenture, F100) | Completed tasks / PRs | **+26.08%** (SE ≈ 10.3%) | Output per developer-period — closest to ours |
| Becker/METR (2025), arXiv 2507.09089 | Within-dev RCT on real OSS issues | 16 OSS maintainers, 246 issues | Time-per-issue | **+19% time** (slowdown; CI $+2\%$ to $+39\%$) | Per-issue time on experienced maintainers of mature OSS |
| Becker, Rush, Cunningham, Rein, Mahamud / METR (Feb 2026 blog update) | Follow-up within-dev RCT, late-2025 data | 57 devs (10 returning + 47 new), 143 repos, 800+ tasks | Time-per-issue | Returning devs: $-18\%$ (CI $-38\%$ to $+9\%$); new devs: $-4\%$ (CI $-15\%$ to $+9\%$). METR: data "too compromised" to be reliable due to control-arm opt-out | Same construct as above; directional reversal but unreliable by METR's own assessment |

### Observational / survey (not triangulation anchors, useful as context)

- **Ziegler et al.\ (2024), CACM.** Survey $+$ telemetry correlation
  ($N = 2{,}631$ Copilot users). No causal effect size; acceptance rate
  correlates with self-reported productivity. Cite for *perception* of
  effect, not magnitude.
- **DORA (2024, 2025).** Large self-report surveys with regression
  decomposition. 2024: $+25\%$ AI adoption associated with $+2.1\%$
  individual productivity but $-1.5\%$ team throughput and $-7.2\%$
  stability; 2025 reports directional reversal at org level but persistent
  stability concerns. Cite as industry-scale descriptive context, not as
  a point estimate.

### Observational DiD-style studies on OSS (methodological cousins, *not* triangulation)

These are OSS-repo panel studies methodologically similar to our own
design. They should be cited as *parallel observational evidence* to
contextualize our DiD, not as independent experimental triangulation:

- Song, Agarwal \& Wen (2024), arXiv 2410.02091 — DiD on Copilot effect in OSS.
- Yeverechyahu, Mayya \& Oestreicher-Singer (2024), ICIS — DiD on
  Copilot-eligible vs.\ ineligible languages.
- Hoffmann, Boysel, Nagle, Peng \& Xu (2024), CESifo WP — quasi-experiment
  on Copilot eligibility.

### What the experimental evidence collectively suggests

1. Direction is consistently positive in short, well-scoped tasks
   (Peng, Paradis), usually measured as per-task time reductions of
   $\sim 20$–$55\%$.
2. At the firm-level with output volume as the outcome, the best
   estimate is Cui et al.\ at $+26\%$ ($\text{SE} \approx 10\%$). This
   is the single study closest in construct to "monthly commits."
3. METR's evidence on experienced OSS maintainers is a moving target.
   The July 2025 preprint (16 devs, 246 issues) reported a $+19\%$
   slowdown (CI $+2\%$ to $+39\%$). A Feb 2026 METR blog update
   reporting late-2025 follow-up data (57 devs, 800+ tasks) found the
   direction reversed — non-significant speedups of $-18\%$
   (returning devs) and $-4\%$ (new devs) — but METR themselves
   characterize the follow-up data as "too compromised" to be
   reliable because control-arm developers increasingly opted out of
   AI-disallowed tasks. Taken together: the effect on experienced
   OSS maintainers of mature codebases is not cleanly identified as
   of early 2026, with a plausible range that crosses zero. This
   heterogeneity warrants acknowledgment in our triangulation
   paragraph but does not contradict a positive population-level ATT
   across a diverse set of $\sim 1{,}000$ OSS repos.
4. Our $+32\%$–$+52\%$ DiD range is consistent with Cui's $+26\%$
   firm-RCT anchor and sits within the wider range established by
   controlled experiments. The naive $+911\%$ is inconsistent with
   every RCT on record by roughly an order of magnitude.

## Key claims the revision will establish

- [ ] The $+32\%$–$+52\%$ ATT range is broadly consistent with the Cui
  et al.\ RCT anchor ($+26\%$) and within the wider controlled-experiment
  range; the $+911\%$ naive estimate is not consistent with any.
- [ ] Magnitudes matter for intervention-appraisal, policy, and
  investment questions. The "direction, not magnitude" defense does not
  apply when the substantive question is "how much."
- [ ] Triangulation across observational and experimental designs is the
  strategy for accumulating credible causal knowledge (already invoked
  in Section 5's conclusion via \citet{angrist2010credibility,
  shadish2002experimental}). The worked example is a concrete instance.
- [ ] Heterogeneity across experimental findings is real and should be
  named. Flag the METR evidence honestly as a moving target — 2025
  preprint found slowdown, 2026 follow-up suggests reversal but is
  flagged by METR itself as unreliable — so the true effect on
  experienced OSS maintainers of mature codebases is not cleanly
  identified.

## Proposed revisions

### Section 4.2 — Longitudinal Takeaway (`sec:longitudinal-takeaway`)

- [ ] Add a paragraph (4–6 sentences) titled implicitly as "external
  triangulation" at the end of the Longitudinal Takeaway. Key moves:
  - Anchor on Cui et al.\ ($+26\%$, three-site firm RCT, $N = 4{,}867$).
    This is the only existing evidence with a comparable construct
    (output per developer-period) and causal design.
  - Note Peng et al.\ and Paradis et al.\ as per-task-time RCTs in the
    same direction but with different constructs; explicitly name the
    construct gap.
  - Cite the METR evidence honestly as a moving target: the July 2025
    preprint's $+19\%$ slowdown on 16 experienced OSS maintainers, and
    the Feb 2026 METR follow-up showing a directional reversal
    ($-4\%$ to $-18\%$) that METR itself flags as unreliable due to
    control-arm attrition. The net message: effects on experienced OSS
    maintainers of mature codebases are not cleanly identified, with a
    plausible range crossing zero. Do not bury this uncertainty.
  - State the punchline: the $+32\%$–$+52\%$ range is consistent with the
    RCT evidence base; $+911\%$ is not.

### Section 4.3 — Summary (near Table 7 discussion)

- [ ] Add one sentence to the existing Table 7 discussion: the
  design-based estimates are not only methodologically defensible, they
  are the only estimates consistent with the magnitude range seen in
  field experiments on AI coding tools
  (Section~\ref{sec:longitudinal-takeaway}).

### Section 5.1 — Lessons from the Worked Example

- [ ] Promote external triangulation to a named lesson. Current lessons
  are (a) design-driven shrinkage, (b) temporal collapse in MSR,
  (c) substantive AI finding. Add (or fold into (c)): *"Design-based
  estimates triangulate with external experimental evidence while
  naive estimates do not."* Two to three sentences. Reuse the Cui et al.
  anchor and METR caveat from §4.2.
- [ ] Pre-empt the "direction, not magnitude" defense. One or two
  sentences making explicit that for intervention-appraisal questions
  (resource allocation, policy investment, technology adoption),
  direction-only inference is inadequate. Link back to the
  estimand-question framing in \citet{lundberg2021estimand}.

### Inline comparison: prose vs. table

- [ ] Decision: **prose only** in §4.2, no new figure or table. A
  separate table risks elevating the triangulation to an
  overemphasized subsection; a prose paragraph with three-to-four
  parenthetical effect sizes conveys the same content while keeping the
  section's focus on methodology. Revisit if the paragraph feels
  cramped.

### Introduction (Section 1)

- [ ] Low priority. Consider one sentence in the contributions list
  noting that the worked example both demonstrates methodology *and*
  produces an AI-tools estimate consistent with experimental evidence.
  Only if it fits naturally.

### FAQ (Appendix C)

- [ ] Add a new Q/A: *"The naive estimate and the DiD estimate have the
  same sign. Does the magnitude really matter?"* Answer in 3–5
  sentences: for policy, investment, and technology-adoption questions
  magnitudes determine decisions; the observational–experimental
  triangulation in the worked example is a concrete illustration.
  Reference Cui et al. and METR for both sides of the range.

### README TLDR

- [ ] Update "Substantive AI Finding" bullet to include the
  triangulation framing once the paper text is settled. Keep README
  downstream of the paper.

## Bibliography additions

Only `DBLP:conf/icse-seip/ParadisGMNMMZFC25` is already in
`paper/references.bib`. The following entries must be added, following
`paper/AGENTS.md` conventions:

- [ ] `peng2023impact` — arXiv 2302.06590. Non-CS section (preprint /
  economics-adjacent). Verify against arXiv.
- [ ] `ziegler2024measuring` — CACM 67(3), 54–63, 2024. DOI
  10.1145/3633453. CS publication — use DBLP key if available. The
  agent's search surfaced DBLP record
  `journals/cacm/ZieglerKLRRSSA24`; verify directly from DBLP BibTeX API
  before adding.
- [ ] `cui2025effects` — NBER WP 33777 / SSRN 4945566 / Management
  Science DOI 10.1287/mnsc.2025.00535. Non-CS. Published version
  preferred.
- [ ] `becker2025measuring` — arXiv 2507.09089 (also METR research
  report, July 2025). Non-CS preprint.
- [ ] `metr2026uplift` — online/institutional resource. METR blog
  update, 2026-02-24, "We are Changing our Developer Productivity
  Experiment Design" (Becker, Rush, Cunningham, Rein, Mahamud).
  Include access date. URL:
  https://metr.org/blog/2026-02-24-uplift-update/.
- [ ] `dora2024state` and `dora2025state` — online/institutional
  resources. Include access date and URL.

Tasks:

- [ ] Verify each entry against primary source (DBLP API for the CS
  entry; DOI landing pages for the rest). Do not rely on the sweep
  report's BibTeX blocks verbatim — re-verify before committing.
- [ ] For Peng et al., retrieve the reported SE/CI from the paper's
  regression table before printing any CI in text. The sweep confirmed
  the $-55.8\%$ point estimate but could not extract the CI reliably.
- [ ] For Becker/METR, read Appendix D for clustered SEs before printing
  a CI. The arXiv abstract does not state one.

## Writing guidelines

- **Tone.** Measured and comparative, not triumphalist. The DiD estimate
  is a plausible point estimate, not a definitive one. Avoid framings
  that imply the design-based estimate is "correct" and the naive
  estimate is "wrong"; say instead that the naive estimate is inflated
  by mechanisms the toolkit identifies and removes.
- **Measurement honesty.** Controlled experiments measure task-completion
  time or short-horizon individual output; our DiD measures
  project-level monthly commits. The constructs are related but not
  identical. Every triangulation sentence must acknowledge this without
  undercutting the broader directional agreement.
- **Heterogeneity honesty.** METR's contrarian finding must appear in
  the triangulation paragraph, not in a footnote. The tutorial's
  credibility depends on acknowledging the full range rather than
  cherry-picking.
- **Follow AGENTS.md respectful framing.** Do not disparage prior
  observational AI-tools studies that report large cross-sectional
  effects; frame them as illustrating the identification gap this
  tutorial addresses.

## Risks and caveats

- **Overclaiming alignment.** Cui at $+26\%$ and our DiD at $+32\%$–$+52\%$
  are in the same order of magnitude but not numerically identical. The
  prose must describe this as "consistent with" or "in the ballpark of,"
  not "matches." Given METR's contrarian finding on a different
  subpopulation, even this claim is conditional.
- **Construct mismatch.** Task-time RCTs and our commit-count DiD are
  different constructs. The triangulation argument rests on directional
  and order-of-magnitude agreement, not on cross-construct conversion.
- **Scope creep.** This is a pedagogical worked example, not an AI-tools
  meta-analysis. Resist expanding the literature discussion beyond what
  is needed to establish the triangulation point and acknowledge
  heterogeneity.
- **Publication-date alignment.** METR (2025) and Cui et al.\ (Management
  Science 2025) are recent; be careful not to cite superseded working
  paper numbers where a published version exists.

## Out of scope

- A full meta-analysis of AI coding tool effects.
- Re-running the DiD with alternative outcomes (PRs merged, lines
  changed).
- Quantitative reconciliation with any specific external study.
- Re-examining the observational DiD-style OSS studies (Song,
  Yeverechyahu, Hoffmann) as independent evidence — they share our
  design family and should be cited as *parallel observational* rather
  than *triangulating experimental* evidence.
