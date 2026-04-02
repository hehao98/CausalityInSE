# Cross-Sectional AI Coding Tool Adoption Example

**Created:** 2026-04-01
**Purpose:** Replace Example B (Bogner & Merkel JS vs. TS) with a fresh, topical cross-sectional study of AI coding tool adoption across popular GitHub repositories. Pairs with Example C (Cursor ITS/DiD) to form the diagnostic-then-constructive arc.

---

## Motivation and Pedagogical Role

The current Example B (Bogner & Merkel) demonstrates the cross-sectional ceiling: DAG-guided covariate selection, OVB fragility, and PSM/IPW convergence all show that the estimator is not the bottleneck --- unobserved confounding is. A new AI coding tool adoption example would deliver the same lesson in a domain that:

1. **Thematically unifies with Example C (Cursor ITS/DiD):** Both examples are about AI coding tools. The new example asks "Do repos that adopt AI coding agents have higher development productivity?" cross-sectionally; Example C asks "What happens to productivity and quality when a repo adopts Cursor?" longitudinally. The pairing is natural: cross-sectional → "we cannot tell" → longitudinal → "now we can, and the sign flips on quality."
2. **Is timely and broadly engaging:** AI-assisted development is the most active topic in SE. Readers will immediately see the relevance.
3. **Illustrates selection bias in a vivid, intuitive setting:** The selection story is obvious: well-maintained repos with active, tech-savvy developers are *more likely* to adopt AI tools *and* more likely to have high commit activity. Any cross-sectional association between AI adoption and productivity is deeply confounded.
4. **Uses publicly available, reproducible data:** GitHub API + file-path-based AI maturity classification (no proprietary data needed). The primary outcome --- monthly commits --- requires no cloning or static analysis tooling.

---

## Overview of the Plan

```
Phase 1: Data Collection
  ├── 1a. Fetch top repos by stars across 10 languages
  ├── 1b. Collect repo-level covariates from GitHub API
  └── 1c. Classify AI maturity level (L1--L4) via file-path scanning

Phase 2: Exploratory Analysis
  ├── 2a. Descriptive statistics and covariate balance
  └── 2b. Construct DAG for AI adoption → code quality

Phase 3: Cross-Sectional Analysis (Diagnostic Arc)
  ├── 3a. Naive group comparison (L1 vs. L2+)
  ├── 3b. DAG-guided OLS with covariate selection
  ├── 3c. Kitchen-sink OLS and OVB diagnostics
  ├── 3d. PSM and IPW under DAG-justified covariates
  └── 3e. Cross-sectional ceiling argument

Phase 4: Write-Up for Section 4.x
```

---

## Phase 1: Data Collection

### 1a. Fetch Top Repositories by Stars Across 10 Languages

**Languages (10):** Python, JavaScript, TypeScript, Java, C++, C, Go, Rust, Ruby, Swift

These represent a mix of established and modern languages, spanning systems programming, web development, and general-purpose domains. All have large GitHub ecosystems.

**Sampling strategy:**
- For each language, fetch the top 100 repositories by star count using the GitHub Search API (`GET /search/repositories?q=language:{lang}&sort=stars&order=desc`).
- Total: ~1,000 repos (10 languages x 100 repos).
- **Exclusion criteria:**
  - Forks (exclude via `fork:false` in query)
  - Archived repositories
  - Repos with fewer than 50 commits (too small to meaningfully assess quality)
  - Repos that are primarily documentation, awesome-lists, or tutorial collections (filter by topic or manual inspection of top results)
- **Deduplication:** Some repos may appear under multiple languages (e.g., a repo with both Python and C++). Assign each repo to its *primary* language (the one GitHub reports as dominant).

**Expected yield:** ~800--900 repos after filtering.

### 1b. Collect Repo-Level Covariates from GitHub API

For each repo, collect the following observable covariates via the GitHub REST/GraphQL API:

| Covariate | API Source | Rationale |
|-----------|-----------|-----------|
| **Stars** | `stargazers_count` | Proxy for popularity/visibility |
| **Forks** | `forks_count` | Proxy for community engagement |
| **Open issues** | `open_issues_count` | Maintenance signal |
| **Watchers** | `subscribers_count` | Attention signal |
| **Creation date** | `created_at` | Repo age |
| **Last push date** | `pushed_at` | Recency of activity |
| **Primary language** | `language` | Stratification variable |
| **License** | `license.spdx_id` | Governance signal |
| **Has wiki** | `has_wiki` | Documentation maturity |
| **Has discussions** | `has_discussions` | Community infrastructure |
| **Default branch protection** | Branch protection API | Governance signal |
| **Number of contributors** | Contributors API (paginated count) | Team size proxy |
| **Total commits** | `GET /repos/{owner}/{repo}/commits?per_page=1` + parse `Link` header for count, or use GraphQL `defaultBranchRef.target.history.totalCount` | Activity level |
| **Repo size (KB)** | `size` | Codebase scale |
| **Topics/tags** | `topics` | Domain classification |
| **Organization vs. personal** | `owner.type` | Governance structure |
| **Has CI/CD** | Check for `.github/workflows/` presence | Engineering maturity |
| **Total PRs** | GraphQL `pullRequests.totalCount` | Development process signal; repos using PR workflows differ systematically |
| **Total issues** | GraphQL `issues.totalCount` | Community engagement / issue-tracking maturity |
| **Number of releases** | Releases API | Maturity signal |

**Productivity outcome (primary):**

| Outcome | Source | Notes |
|---------|--------|-------|
| **Monthly commits** | GraphQL API: `defaultBranchRef.target.history` with `since`/`until` filters, or REST Commits API with date range | Primary outcome. Compute for a recent window (e.g., last 6 months). Average monthly commits gives a single cross-sectional measure per repo. |
| **Monthly PRs merged** | GraphQL `pullRequests(states: MERGED)` with date filter | Supplementary velocity measure; captures review-gated workflow |

Monthly commits is directly available from the GitHub API, requires no cloning or static analysis tooling, and connects naturally to Example C where Cursor's velocity effect (commits, lines added) is the robust finding across all specifications. The outcome also has a clear, intuitive interpretation: "Do repos with AI tool adoption produce more commits per month?"

**Note on code quality outcomes:** Assessing code quality at scale would require running SonarQube or language-specific linters on ~900 repos across 10 languages --- expensive and brittle. We deliberately set this aside. If the cross-sectional ceiling argument holds for productivity (which has better measurement properties), it holds a fortiori for noisier quality proxies.

### 1c. Classify AI Maturity Level via File-Path Scanning

For each repo, determine the AI maturity level (L1--L4) using the file-path-based classification rules provided in the prompt.

**Implementation options (in order of preference):**

1. **GitHub Trees API (`GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1`):** Returns the full file tree without cloning. Match file paths against L2/L3/L4 patterns. Fast and rate-limit-friendly (one call per repo).
2. **GitHub Contents API:** Check for specific files/directories. More targeted but requires multiple calls per repo.
3. **Clone and scan:** Most thorough but slowest. Reserve for repos where the Trees API truncates (>100K files).

**AI contributor signals (supplementary):**
In addition to file-path-based classification, check whether known AI bot accounts have contributed to the repo:
- `dependabot[bot]` (not AI coding, exclude)
- `github-actions[bot]` (not AI coding, exclude)
- `copilot` or `github-copilot` contributor activity (if detectable)
- `claude-ai`, `devin-ai`, `sweep-ai`, `coderabbit-ai`, or similar bot accounts in contributor list or PR authors
- Commit author names/emails matching AI tool patterns (e.g., `noreply@anthropic.com`, `devin@cognition.ai`)

Check contributors via `GET /repos/{owner}/{repo}/contributors` and recent PR authors via the GraphQL API.

**Treatment definition:**
- **Binary treatment (primary):** L2+ (any AI tool configuration) vs. L1 (no AI artifacts). This is the cleanest treatment for regression/PSM/IPW.
- **Ordinal treatment (secondary):** L1 < L2 < L3 < L4. Useful for dose-response exploration but complicates identification.
- **AI contributor (supplementary):** Whether an AI bot has authored commits or PRs. Captures *active* agentic use beyond configuration files.

---

## Phase 2: Exploratory Analysis

### 2a. Descriptive Statistics and Covariate Balance

- Tabulate the distribution of AI maturity levels across languages and overall.
- Compare covariate distributions between L1 (no AI) and L2+ (AI adopters) repos.
- Report standardized mean differences (SMDs) for all covariates. Expect severe imbalance: AI-adopting repos are likely newer, more popular, more actively maintained, and in trendier languages (TypeScript, Rust, Go).
- Visualize the overlap (or lack thereof) in propensity score distributions.

### 2b. Construct DAG for AI Adoption and Code Quality

Propose a causal DAG encoding the assumed data-generating process:

```
                    ┌────────────┐
                    │  Developer │
                    │   Skill    │
                    └──┬─────┬───┘
                       │     │
                       ▼     ▼
┌──────────┐     ┌─────────────┐     ┌──────────────┐
│  Repo    │────►│  AI Tool    │────►│  Monthly     │
│  Age     │     │  Adoption   │     │  Commits     │
└──────────┘     └─────────────┘     └──────────────┘
                       ▲     ▲              ▲
                       │     │              │
                 ┌─────┘     └────┐         │
                 │                │         │
           ┌─────────┐    ┌──────────┐     │
           │  Org     │    │ Project  │     │
           │ Culture  │    │ Maturity │─────┘
           └─────────┘    └──────────┘
                                ▲
                                │
                          ┌───────────┐
                          │  Language │
                          │  Choice   │
                          └───────────┘
```

Key causal relationships to encode:
- **Confounders (common causes of AI adoption AND monthly commits):**
  - Developer skill / team experience (unobserved): skilled, active developers both adopt AI tools and commit more frequently.
  - Organizational culture / governance (partially observed via org type, branch protection): well-resourced orgs invest in tooling *and* sustain high commit velocity.
  - Project maturity / activity level (observed via age, size, contributors): mature, active projects both adopt AI tools and have higher baseline commit rates.
  - Language ecosystem (observed): some languages (TypeScript, Rust) have stronger AI tooling ecosystems and more active developer communities.
- **Collider candidates:**
  - Stars / popularity: caused by both high commit activity (active repos attract stars) and AI adoption hype (AI-configured repos get attention). Conditioning on it risks Berkson's paradox.
- **Post-treatment variables:**
  - Number of contributors may increase *because* of AI tool adoption (lower barrier to entry). Conditioning on it would attenuate the treatment effect.
- **Reverse causality:**
  - High commit velocity may *attract* AI tool adoption (active repos have more reason to invest in developer tooling), rather than the reverse. Cross-sectional data cannot distinguish the causal direction.

**DAG-guided covariate selection:**
- **Condition on:** repo age, primary language, organization type, CI/CD presence, license type, repo size (KB), number of releases (pre-treatment maturity signals).
- **Do NOT condition on:** stars (collider risk), current contributor count (post-treatment risk).
- **Cannot observe:** developer skill, team culture, intrinsic development discipline.

---

## Phase 3: Cross-Sectional Analysis (Diagnostic Arc)

The analysis follows the same four-stage structure as Example B (Bogner & Merkel), demonstrating that the diagnostic framework is general:

### Stage 1: Naive Group Comparison

Compare mean monthly commits between L1 and L2+ repos:
- Raw mean comparison (t-test or Wilcoxon)
- Distribution visualization (density plots, box plots by AI maturity level)
- By-language breakdown to check consistency

**Expected result:** L2+ repos likely show *higher* monthly commits in naive comparison, because the same factors that predict AI adoption (active maintenance, skilled developers, well-resourced organizations) also predict high commit velocity. The association is real but causally uninterpretable.

### Stage 2: DAG-Guided OLS vs. Kitchen-Sink OLS + OVB Diagnostics

Two specifications:
- **M_dag:** `log_monthly_commits ~ ai_adoption + repo_age + language + org_type + has_ci + license_type + log_size + log_releases`
  - Only DAG-justified confounders.
- **M_all:** `log_monthly_commits ~ ai_adoption + repo_age + language + org_type + has_ci + license_type + log_size + log_releases + log_stars + log_forks + log_contributors + log_total_prs + log_total_issues`
  - Kitchen-sink including collider (stars) and post-treatment variables.

**OVB diagnostics:**
- **Coefficient stability:** Track how the AI adoption coefficient changes as controls are added. Expect attenuation (as with Bogner & Merkel).
- **Cinelli & Hazlett robustness values (sensemakr):** Assess how strong an unobserved confounder would need to be to explain away the remaining effect. Expect small RVs given the obvious unobserved confounders (developer skill).
- **Oster proportional selection bounds:** Assess how much selection on unobservables (relative to observables) is needed to drive the coefficient to zero.

### Stage 3: PSM and IPW Under DAG-Justified Covariates

- **Propensity Score Matching (PSM):** 1:1 nearest-neighbor matching on DAG-justified covariates. Report matched-sample estimates and balance diagnostics.
- **Inverse Probability Weighting (IPW):** Weight L1 repos to resemble L2+ repos on DAG-justified covariates. Report effective sample size and weighted estimates.

**Expected result:** Three estimators (OLS, PSM, IPW) converge on similar point estimates with similar fragility --- demonstrating, as in Example B, that the *estimator is not the bottleneck*.

### Stage 4: The Cross-Sectional Ceiling Argument

Argue that no amount of cross-sectional sophistication can separate:
- "AI tools increase development productivity" (causal)
- "Productive teams adopt AI tools" (reverse causality / selection)
- "Active, well-resourced projects both adopt AI tools and produce many commits" (confounding)

The unobserved confounders (developer skill, team culture, organizational investment in tooling) are the binding constraint, not the choice of OLS vs. PSM vs. IPW.

**Transition to Example C:** This is precisely why longitudinal data is needed. Example C (Cursor ITS/DiD) exploits within-repo temporal variation: the same repo before and after Cursor adoption. Repo FE absorbs all time-invariant confounders --- exactly the ones that make the cross-sectional analysis fail. Notably, the velocity effect (commits, lines added) is the *robust* finding in Example C --- it survives across all specifications including the full DiD. But the quality outcomes flip sign under FE, demonstrating that even when productivity effects are genuine, cross-sectional designs cannot distinguish them from selection.

---

## Phase 4: Write-Up for Section 4.x

The narrative structure mirrors the current Example B plan:

1. **Setup:** Motivate the question --- "Does adopting AI coding tools increase development productivity?" --- and frame it as a target trial.
2. **DAG:** Present the causal DAG, identify confounders, colliders, reverse causality, and unobservables.
3. **Naive comparison:** Show the raw association (AI adopters have higher monthly commits).
4. **Diagnostic progression:** Walk through OLS → OVB → PSM/IPW, showing convergence and fragility.
5. **Ceiling:** Conclude that cross-sectional data cannot answer this question.
6. **Bridge to Example C:** "We need within-repo temporal variation --- which is exactly what the Cursor natural experiment provides. There, the velocity effect survives all specifications, but the quality effect *flips sign* --- a lesson only longitudinal data can teach."

---

## Implementation Details

### Data Collection Scripts

Create an R Markdown notebook (`notebooks/ai_adoption_cross_sectional.Rmd`) or a Python script (`scripts/collect_ai_adoption_data.py`) that:

1. Queries GitHub Search API for top repos per language.
2. Fetches covariates via REST/GraphQL API.
3. Fetches file trees and classifies AI maturity levels.
4. Checks for AI bot contributors.
5. Computes monthly commit counts for the outcome window (e.g., last 6 months).
6. Saves the dataset to `data/` (or the data submodule).

### Rate Limiting

GitHub API rate limits: 5,000 requests/hour (authenticated). Budget:
- Search queries: 10 (one per language)
- Repo metadata: ~1,000 (one per repo, already fetched in search)
- File trees: ~1,000 (one per repo)
- Contributors: ~1,000 (one per repo)
- Monthly commit counts: ~6,000 (one per repo per month for a 6-month window via GraphQL `history(since, until)` with `totalCount`)
- Total PRs and issues: ~2,000 (one per repo each via GraphQL)
- Total: ~12,000 requests. Fits within 2--3 hours with a single token, or use GraphQL batching to reduce call count.

**Alternative:** Use GH Archive for commit time series if API rate limits are prohibitive.

### Analysis Notebook

Create `notebooks/ai_adoption_cross_sectional.Rmd` (following existing notebook conventions):
- Stage 1: Descriptive statistics, covariate balance tables, SMD plots.
- Stage 2: OLS models (M_dag, M_all), coefficient stability plots, sensemakr/Oster diagnostics.
- Stage 3: PSM (MatchIt), IPW, three-estimator comparison table.
- Stage 4: Narrative summary and cross-sectional ceiling argument.

---

## Task Checklist

### Data Collection
- [ ] Write GitHub API data collection script (top 100 repos x 10 languages)
- [ ] Implement AI maturity classification (L1--L4) via file tree scanning
- [ ] Implement AI bot contributor detection
- [ ] Collect repo-level covariates (stars, age, contributors, size, total PRs, total issues, etc.)
- [ ] Compute monthly commit counts for outcome window (last 6 months)
- [ ] Apply exclusion criteria and deduplicate
- [ ] Save cleaned dataset

### Exploratory Analysis
- [ ] Tabulate AI maturity level distribution by language
- [ ] Compute and visualize covariate balance (SMDs) between L1 and L2+
- [ ] Finalize DAG for AI adoption → monthly commits

### Cross-Sectional Diagnostic Analysis
- [ ] Stage 1: Naive group comparison
- [ ] Stage 2: DAG-guided OLS, kitchen-sink OLS, OVB diagnostics (sensemakr, Oster)
- [ ] Stage 3: PSM (MatchIt) and IPW, three-estimator convergence table
- [ ] Stage 4: Cross-sectional ceiling argument

### Write-Up
- [ ] Draft Section 4.x narrative (diagnostic arc for AI adoption example)
- [ ] Draft transition paragraph bridging to Example C (Cursor ITS/DiD)

---

## Risks and Mitigations

1. **Low AI adoption prevalence:** If very few top-starred repos have AI config files (L2+), the treatment group will be small and estimates underpowered.
   - *Mitigation:* Top-starred repos are likely *more* likely to adopt AI tools. If prevalence is still low, expand to top 200 per language or lower the star threshold.
   - *Mitigation:* Use the AI bot contributor signal as a supplementary treatment definition.

2. **AI adoption is very recent:** Most AI config files (CLAUDE.md, .cursorrules) appeared in 2024--2026. Monthly commit counts reflect overall project activity, not just post-adoption productivity.
   - *Mitigation:* This is *exactly the point* --- cross-sectional data cannot separate pre- and post-treatment productivity. The temporal mismatch strengthens the ceiling argument.

3. **Outcome reflects project scale, not AI effect:** Monthly commits is driven primarily by team size, project maturity, and domain --- not by AI tool adoption.
   - *Mitigation:* This confounding is the pedagogical lesson. After controlling for observable project characteristics, the remaining association is still uninterpretable because developer skill and organizational investment are unobserved. Monthly PRs merged can serve as a supplementary outcome.

4. **GitHub API rate limits:** ~4,000+ API calls needed.
   - *Mitigation:* Use authenticated requests; batch with GraphQL where possible; cache aggressively; spread collection over multiple hours if needed.

5. **Confounding with repo popularity:** Top-starred repos are unusual; they may not be representative of the broader GitHub population.
   - *Mitigation:* Acknowledge external validity limitation. The goal is pedagogical demonstration, not population inference. The *within-sample* confounding (selection into AI adoption) is the central lesson.
