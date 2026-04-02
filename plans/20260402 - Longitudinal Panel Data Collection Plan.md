# Longitudinal Monthly Panel Data Collection Plan

**Created:** 2026-04-02
**Purpose:** Extend the cross-sectional AI adoption dataset (1,000 repos) into a balanced monthly panel from 2024-01 through 2026-03 (27 months). This panel enables a staggered difference-in-differences or event-study design that exploits within-repo temporal variation in AI tool adoption.

---

## Design Overview

| Element | Specification |
|---------|--------------|
| **Unit** | Repository (same 1,000 repos from cross-sectional study) |
| **Time** | Monthly, 2024-01 through 2026-03 (27 months) |
| **Panel size** | ~1,000 repos × 27 months ≈ 27,000 repo-month observations |
| **Outcome** | Monthly commit count on default branch |
| **Treatment** | Binary absorbing: first month a repo contains an L2+ AI config file (staggered adoption) |
| **Time-varying confounders** | New stars, new issues, active contributors, new forks, new releases (per month). PRs merged collected but likely excluded from primary model. |

---

## Git-Based Extraction: Treatment Timing, Monthly Commits, and Contributors

Instead of relying on the GitHub API for commits, contributors, and treatment timing, we **clone all 1,000 repos** and extract everything directly from git history. This is simpler, more reliable (no pagination, no rate limits), and gives us exact author-level metadata.

### Clone Strategy

```bash
# Blobless bare clone: downloads commits + trees but skips file contents.
# Sufficient for git log (dates, authors, file paths) without downloading blobs.
git clone --filter=blob:none --bare https://github.com/{owner}/{repo}.git
```

- **Disk estimate:** ~10-100 MB per bare blobless clone × 1,000 repos ≈ **~50 GB total**
- **Time estimate:** ~10-60 seconds per clone; parallelised across 8 workers ≈ **~1-2 hours**
- **Storage location:** a scratch directory (e.g., `/data2/haohe/repos_bare/`)

### Treatment Variable: Date of First L2+ File

For each repo, search git history for the earliest commit that added any known AI config file pattern:

```bash
git log --diff-filter=A --format='%H %aI' --reverse -- \
  '.cursorrules' '.cursor/rules' 'CLAUDE.md' '.claude/*' \
  '.github/copilot-instructions.md' '.windsurfrules' \
  '.aider*' '.coderabbit*' 'codegen.yml' \
  | head -1
```

- `--diff-filter=A`: only commits that **added** a file matching the pattern
- `--reverse | head -1`: earliest such commit
- Extract the author date → assign `treatment_month` (YYYY-MM)
- For repos where no match is found, `treatment_month = NA` (never-treated / L1)

**Edge cases:**
- Files added and then removed: still counts as first adoption (intent-to-treat).
- Files added before 2024-01: treatment is "always-treated" for the full panel window. These repos contribute to identification only if we can find a pre-treatment period in an extended window. Otherwise, they serve as always-treated comparisons.
- Files added after 2026-03: classified as never-treated in our window.

### Outcome Variable: Monthly Commits

Count commits on the default branch per calendar month:

```bash
for year in 2024 2025 2026; do
  for month in $(seq -w 1 12); do
    start="${year}-${month}-01"
    end=$(date -d "${start} +1 month" +%Y-%m-%d)
    count=$(git rev-list --count --after="${start}" --before="${end}" HEAD)
    echo "${repo},${year}-${month},${count}"
  done
done
```

This replaces the GraphQL `history.totalCount` approach — exact same data, zero API calls.

### Monthly Active Contributors

Count unique commit authors per month from the same git log:

```bash
git log --format='%aI %ae' --after='2024-01-01' --before='2026-04-01' | \
  awk '{split($1,d,"-"); month=d[1]"-"d[2]; authors[month][$2]=1}
       END {for (m in authors) print m, length(authors[m])}'
```

This gives us the `active_contributors` time-varying confounder for free — no API needed.

---

## Time-Varying Confounders

### 1. Monthly New Stars (attention/visibility proxy)

Stars measure external attention. A sudden burst of stars (e.g., Hacker News feature, trending on GitHub) independently increases both the likelihood of AI tool adoption (new contributors bring AI config files) and commit velocity (new contributors start committing).

### 2. Monthly New Issues (demand proxy)

New issues represent user demand and bug reports. High issue volume reflects active usage, which independently drives both AI adoption (maintainers seek productivity tools) and commits (more issues → more bug-fix commits).

### 3. Monthly Active Contributors (supply proxy)

Unique commit authors per month. More contributors independently increase commit velocity and the probability that one of them introduces AI tooling. **Extracted directly from the cloned repos** via `git log --format='%aI %ae'` — no API needed.

### 4. Monthly New Forks (community engagement proxy)

Forks indicate new potential contributors. Like stars, a spike in forks reflects external attention that could independently drive both adoption and productivity.

### 5. Monthly Releases/Tags (development cadence proxy)

Release frequency captures development lifecycle rhythm. Projects in active release cycles may both adopt AI tools (to accelerate releases) and produce more commits. Changes in release cadence may indicate organizational decisions that affect both treatment and outcome.

### Other Confounders Considered

| Confounder | Rationale | Feasibility | Decision |
|-----------|-----------|-------------|----------|
| **Monthly PRs merged** | Process intensity; PR-heavy workflows differ systematically | GHArchive `PullRequestEvent` | **Fetch but probably exclude from model** — PRs are tightly coupled with commits (near-post-treatment / mechanistic relationship), so conditioning on them risks blocking the causal path. Collect for exploratory analysis. |
| **Monthly lines changed** | Code churn; high-churn repos may adopt AI and commit more | Only from PushEvent payloads (noisy) or cloning | **Exclude** — too noisy, measurement burden high |
| **Median PR review time** | Team health/velocity signal | Requires fetching individual PR timelines | **Exclude** — expensive, secondary |
| **Dependabot/Renovate activity** | Automation level; automated PRs inflate commits | GHArchive or Contributors API | **Exclude** — can add later if needed |
| **Repo trending status** | Detectable from star spikes; endogenous | Derivable from star time series | **Exclude as separate variable** — captured by star spikes |

---

## Data Source Decision: GitHub API vs. GHArchive

### Cost Comparison

| Variable | Source | Cost |
|----------|--------|------|
| **Monthly commits** | Git clone (`git rev-list --count`) | Free (local computation) |
| **Monthly active contributors** | Git clone (`git log --format='%ae'`) | Free (local computation) |
| **Treatment timing** | Git clone (`git log --diff-filter=A`) | Free (local computation) |
| **Monthly new stars** | Stargazers API: ~500K requests (~100 hours). **Prohibitive.** | BigQuery `WatchEvent`: **~$15 total.** |
| **Monthly new issues** | Issues API: ~5,000 requests (~1 hour). Manageable. | BigQuery `IssuesEvent`: included in same query. |
| **Monthly new forks** | No timestamped API. Expensive. | BigQuery `ForkEvent`: included in same query. |
| **Monthly PRs merged** | GraphQL: ~2,000 queries. Manageable. | BigQuery `PullRequestEvent`: included in same query. |
| **Monthly releases** | Releases API: ~1,000 requests. Trivial. | BigQuery `ReleaseEvent`: included in same query. |

### Recommendation: Git Clone + GHArchive Hybrid

**Clone all 1,000 repos** to extract the three variables that require commit-level history: monthly commits (outcome), active contributors (confounder), and treatment timing. This is free, reliable, and avoids API rate limits entirely.

**Use GHArchive (BigQuery)** for the remaining confounders that are not in git history: stars, issues, forks, PRs merged, and releases. A single BigQuery query covers all five event types across 27 months for ~$15.

**Do NOT use the GitHub API** for any of these variables. The API is only needed for the initial repo list and metadata (already collected in the cross-sectional phase).

### BigQuery Query Sketch

```sql
SELECT
  repo.name AS full_name,
  FORMAT_TIMESTAMP('%Y-%m', created_at) AS month,
  COUNTIF(type = 'WatchEvent') AS new_stars,
  COUNTIF(type = 'IssuesEvent' AND JSON_EXTRACT_SCALAR(payload, '$.action') = 'opened') AS new_issues,
  COUNTIF(type = 'ForkEvent') AS new_forks,
  COUNTIF(type = 'PullRequestEvent' AND JSON_EXTRACT_SCALAR(payload, '$.action') = 'closed'
          AND JSON_EXTRACT_SCALAR(payload, '$.pull_request.merged') = 'true') AS prs_merged,
  COUNTIF(type = 'ReleaseEvent') AS new_releases,
  COUNT(DISTINCT IF(type = 'PushEvent', actor.login, NULL)) AS active_pushers
FROM `githubarchive.day.*`
WHERE
  _TABLE_SUFFIX BETWEEN '20240101' AND '20260331'
  AND repo.name IN (
    -- list of 1,000 repo full_names
    'public-apis/public-apis', 'EbookFoundation/free-programming-books', ...
  )
  AND type IN ('WatchEvent', 'IssuesEvent', 'ForkEvent',
               'PullRequestEvent', 'ReleaseEvent', 'PushEvent')
GROUP BY full_name, month
ORDER BY full_name, month
```

**Note on PRs:** We fetch `prs_merged` from GHArchive at zero marginal cost, but PRs are tightly coupled with commits (they are part of the same development process). Including them as a confounder risks blocking the causal path from AI adoption → commits. They are collected for exploratory analysis and robustness checks, not for the primary model specification.

**Estimated scan:** ~4TB across 810 daily tables. At $5/TB after free tier (1TB), cost ≈ **$15**.

---

## Implementation Plan

### Phase 1: Clone Repos and Extract Git-Based Variables

- [ ] Clone all 1,000 repos as bare blobless clones (`--filter=blob:none --bare`) into a scratch directory, parallelised across 8 workers
- [ ] For each cloned repo, extract:
  - **Monthly commits**: `git rev-list --count --after=... --before=... HEAD` for each of 27 months
  - **Monthly active contributors**: unique `%ae` (author email) per month from `git log --format='%aI %ae'`
  - **Treatment timing**: `git log --diff-filter=A --format='%H %aI' --reverse -- <L2+ patterns> | head -1`
- [ ] Output three CSVs:
  - `data/ai_adoption_panel_commits.csv` — columns: `full_name, month, commits`
  - `data/ai_adoption_panel_contributors.csv` — columns: `full_name, month, active_contributors`
  - `data/ai_adoption_treatment_timing.csv` — columns: `full_name, treatment_date, treatment_month, first_ai_file`

### Phase 2: Time-Varying Confounders (GHArchive via BigQuery)

- [ ] Authenticate with Google Cloud and set up BigQuery project
- [ ] Run the single aggregation query above against `githubarchive.day.*`
- [ ] Download results as CSV
- [ ] Output: `data/ai_adoption_panel_gharchive.csv` with columns `full_name, month, new_stars, new_issues, new_forks, prs_merged, new_releases`

### Phase 4: Panel Assembly

- [ ] Left-join commits, confounders, and treatment timing by `(full_name, month)`
- [ ] Add time-invariant repo characteristics from existing `ai_adoption_repos.csv` (language, org type, creation date, etc.)
- [ ] Construct panel variables:
  - `treated_it`: binary, 1 if `month >= treatment_month` for that repo
  - `months_since_treatment`: event-time variable for event-study plots
  - `post_period`: indicator for the general AI-tool era (e.g., post-2024-06 when most tools matured)
- [ ] Handle missing months (repos with zero events in a month should be explicit zeros, not missing)
- [ ] Output: `data/ai_adoption_panel.csv` — the final analysis-ready panel

### Phase 5: Validation

- [ ] Verify panel balance: each repo should have exactly 27 rows
- [ ] Cross-check monthly commits against cross-sectional totals for the overlapping 6-month window
- [ ] Spot-check a few repos' treatment dates against manual GitHub inspection
- [ ] Check GHArchive star counts against known total stars (cumulative sum should approximate current `stargazers_count`)

---

## Identification Strategy Preview

The longitudinal panel enables several designs that the cross-section cannot:

1. **Two-way fixed effects (TWFE):** `commits_it = α_i + γ_t + β·treated_it + δ·X_it + ε_it`
   - Repo FE (α_i) absorbs all time-invariant confounders (language, org culture, developer skill baseline)
   - Month FE (γ_t) absorbs common temporal shocks (GitHub platform changes, seasonal patterns)
   - β identified from within-repo, within-period variation

2. **Event-study specification:** Leads and lags around treatment onset to:
   - Test parallel pre-trends (are treated and control repos on the same trajectory before adoption?)
   - Visualize dynamic treatment effects (does the effect appear immediately or gradually?)

3. **Staggered DiD (Callaway & Sant'Anna or Sun & Abraham):** If treatment timing is heterogeneous (likely — repos adopt AI tools at different times throughout 2024-2025), TWFE can be biased. Modern staggered DiD estimators handle this correctly.

4. **Time-varying confounders (X_it):** Stars, issues, contributors, forks, and releases control for repo-specific shocks that vary over time — the remaining threat after FE absorbs time-invariant confounders. PRs merged are collected but excluded from the primary specification because they are mechanistically downstream of commits (conditioning on them would block the causal path).

---

## Risks and Mitigations

1. **Treatment timing misidentification:** The first L2+ commit may not be the actual adoption date (e.g., file added retroactively or by a drive-by contributor).
   - *Mitigation:* Check whether the commit message or PR context confirms intentional adoption. Flag cases where the AI config was added in a large batch commit.

2. **GHArchive coverage gaps:** Some events may be missing (GHArchive has had occasional outages).
   - *Mitigation:* Check for months with anomalously low event counts across all repos; impute or flag.

3. **Repos created after 2024-01:** Some repos in our sample may not exist for the full 27-month window.
   - *Mitigation:* The panel is unbalanced for these repos (they enter when created). This is fine for FE estimation but should be documented.

4. **Google Cloud / BigQuery setup:** Requires a GCP account with billing enabled.
   - *Mitigation:* The free tier (1TB/month) covers much of the cost; total estimated cost is ~$15.

5. **Parallel trends assumption may fail:** Repos that adopt AI tools may already be on a different productivity trajectory before adoption (e.g., accelerating activity that both attracts AI tools and inflates commits).
   - *Mitigation:* The event-study plot directly tests this. If pre-trends are non-parallel, the DiD is invalid — which is itself an important finding.

---

## Estimated Total Cost and Time

| Component | Method | Time | Cost |
|-----------|--------|------|------|
| Clone 1,000 repos (bare blobless) | `git clone --filter=blob:none --bare` × 8 workers | ~1-2 hours | Free |
| Extract commits, contributors, treatment timing | `git log` / `git rev-list` on local clones | ~30 min | Free |
| Stars, issues, forks, PRs, releases | BigQuery (GHArchive) — 1 query | ~minutes | ~$15 |
| Panel assembly + validation | Local computation | ~1 hour | Free |
| **Total** | | **~3-4 hours** | **~$15** |
| **Disk space** | Bare blobless clones | | **~50 GB** |
