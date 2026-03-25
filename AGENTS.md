# AI Agent Instructions

## Bibliography Management Conventions

When editing or adding entries to BibTeX (`.bib`) files, adhere to the following conventions:

### 1. Document Structure & Ordering

The bibliography is separated into three main sections:
1. **ONLINE / INSTITUTIONAL RESOURCES**: Placed first in the file (e.g., Nobel Prize announcements, W3C standards).
2. **NON-CS PUBLICATIONS**: Placed second in the file.
3. **CS PUBLICATIONS**: Placed third in the file.

#### Sorting Rules
Within each section, entries must be sorted:
1. **Chronologically** by publication year (ascending).
2. **Alphabetically** by the first author's surname (for entries within the same year).

### 2. Citation Keys

#### Online / Institutional Resources
- Use **Google Scholar style** keys or descriptive keys.
- Example: `nobelprize2021economics`, `w3c2023standard`.

#### Non-CS Publications
- Use **Google Scholar style** keys: `surname(s)YYYYkeyword`.
- Example: `hill1965environment`, `angrist2010credibility`.

#### CS Publications
- Use **DBLP identifiers** whenever available.
- Example: `DBLP:conf/sigsoft/RayPFD14`.
- **Verbatim entries**: You MUST retrieve entries directly from the DBLP BibTeX export API (`https://dblp.org/rec/<key>.bib`) or the DBLP website whenever possible. Ensure the entry matches the actual DBLP record.
- **Not yet indexed**: If a paper is not yet indexed by DBLP, assign a manual DBLP-style key and explicitly mark it with a comment directly above the entry (e.g., `% Not yet indexed by DBLP as of 2026-03-19.`).

### 3. Verification Requirement
- **DBLP Entries**: You MUST fetch and verify all DBLP entries against the official DBLP website or API. Do not hallucinate or guess DBLP entries.
- **Google Scholar Entries**: You MUST double-check and verify that all non-CS (Google Scholar style) entries actually exist and the metadata is accurate before adding them.
- **Online / Institutional Resources**: You MUST verify that the URL is accessible and the metadata (author, year, title) is accurate before adding them.

### 4. Metadata Requirements

- **DOIs**: Always include the DOI (`doi={...}`) whenever it is available for a given paper.

### 5. Examples

#### ❌ BAD
```bibtex
@article{Smith2023,
  title={Some Software Engineering Paper},
  author={Smith, John},
  year={2023}
}
```

#### ✅ GOOD (Online / Institutional Resource)
```bibtex
@online{nobelprize2021economics,
  author={{The Royal Swedish Academy of Sciences}},
  title={The {Sveriges Riksbank} Prize in Economic Sciences in Memory of {Alfred Nobel} 2021},
  year={2021},
  url={https://www.nobelprize.org/prizes/economic-sciences/2021/summary/},
  note={Accessed 2026-03-20}
}
```

#### ✅ GOOD (Non-CS Publication)
```bibtex
@article{hill1965environment,
  title={The Environment and Disease: Association or Causation?},
  author={Hill, Austin Bradford},
  journal={Proceedings of the Royal Society of Medicine},
  volume={58},
  number={5},
  pages={295--300},
  year={1965},
  publisher={SAGE Publications}
}
```

#### ✅ GOOD (CS Publication)
```bibtex
@inproceedings{DBLP:conf/sigsoft/RayPFD14,
  author = {Baishakhi Ray and
    Daryl Posnett and
    Vladimir Filkov and
    Premkumar T. Devanbu},
  title = {A large scale study of programming languages and code quality in github},
  booktitle = {Proceedings of the 22nd {ACM} {SIGSOFT} International Symposium on Foundations of Software Engineering},
  year = {2014},
  doi = {10.1145/2635868.2635922}
}
```

## Data Analysis and Plotting Conventions

When creating or modifying plots (e.g., using `ggplot2`) in R scripts and R Markdown files, adhere to the following stylistic guidelines to ensure consistency across the final paper.

### Typography and Fonts

- **Font Family**: Always use **Linux Libertine** (`family = "Linux Libertine"`) for all text elements in the plot (axes, legends, titles, and `geom_text` labels). This matches the ACM LaTeX template.
- **Base Size**: Use `base_size = 13` in your theme (e.g., `theme_minimal(base_size = 13, base_family = "Linux Libertine")`).

### Text Casing

- **Axis Labels**: Use **Title Case** for axis titles (e.g., "Number of Papers", not "Number of papers").
- **Legends**: Use **Sentence case** for legend items and titles (e.g., "Using causal methods", "Asking causal RQs", "All papers"). Acronyms like SE or MSR can remain capitalized.

### Figure Sizing and Theme

To ensure plots look consistent and share the same aesthetic in the final paper, base your styling on the `causal_trends` figure:
- **Save Dimensions**: When saving with `ggsave()`, use `width = 8, height = 3` (or proportionally similar dimensions if a different aspect ratio is strictly required by the plot content).
- **Legend Formatting**: Position the legend at the bottom, share the same font size as the y-axis, and reduce vertical spacing:
 ```R
 theme(
   legend.position = "bottom",
   legend.margin = margin(t = -5, r = 0, b = -3, l = 0),
   legend.box.margin = margin(t = -5, r = 0, b = -3, l = 0),
   axis.title.y = element_text(size = rel(0.8))
 )
 ```
- **Grid Lines**: Remove vertical grid lines if they do not serve a useful purpose (e.g., `panel.grid.major.x = element_blank()`, `panel.grid.minor.x = element_blank()`).

## Git Commit Message Standards

When generating git commit messages, you MUST adhere to the following formatting rules:

1. **Title Length Limit**: The first line (title/subject) MUST be 80 characters or fewer.
2. **Title Style**: Use imperative mood for the title (e.g., "Add feature" not "Added feature" or "Adds feature").
3. **Empty Line**: Leave the second line completely blank.
4. **Detailed Description**: Provide a detailed description starting on the third line.
5. **Body Wrapping**: Wrap the body text at 80 characters for better readability.
6. **Content**: Explain *why* the change is being made and *what* it does, not just how it's implemented.

### Examples

❌ **BAD** (Title too long, no empty line, descriptive mood)
```text
Added the new user authentication module and fixed the login bug that was causing users to be logged out randomly when navigating between pages
Now the system uses JWT tokens with a 24-hour expiration instead of session cookies. I also updated the database schema to store refresh tokens.
```

✅ **GOOD**
```text
Add JWT-based user authentication and fix session dropping

Replace the legacy session-cookie authentication system with JWT tokens
(24-hour expiration) to resolve the bug where users are randomly logged out
during page navigation.

Updates the database schema to securely store and validate refresh tokens.
```

## Plan Management Convention

- All specialized project plans, such as literature review and methodology plans, must be stored in the `plans/` directory.
- The task backlog, however, should be kept in the main `README.md`.
- Use the naming convention `YYYYMMDD - {Few Words Plan Summary}.md` for all plan files (e.g., `260323 - Literature Review Plan.md`).
- Do not store detailed sub-plans directly in the `README.md`. Instead, leave a pointer in `README.md` and place the detailed plan in the `plans/` directory.
- Each plan file should concisely describe the status of tasks, with checked and unchecked markdown checklists.

## Paper Writing Style and Formatting

### One Sentence Per Line

When writing or editing LaTeX (`.tex`) files or documentation, ensure that each sentence is placed on a new line.

#### Why

This practice greatly facilitates version control (`git diff`). When multiple people edit the same paragraph, line-by-line diffs become much cleaner and easier to review if every sentence is on its own line.

#### Rules

- Place a line break after sentence-ending punctuation (e.g., periods, question marks, exclamation marks) instead of continuing on the same line.
- Do not wrap lines or break lines in the middle of a sentence simply to enforce a column width limit.
- Only break mid-sentence if it is dictated by specific formatting constraints (like macros or math formulas that require it).
- Empty lines are still used to separate paragraphs.

#### Examples

##### ❌ BAD
```latex
Empirical software engineering research frequently investigates causal questions. This disconnect between causal ambition and methodological practice mirrors a well-documented crisis in psychology and health research, but the SE community lacks an accessible, unified introduction to the causal inference toolkit. This tutorial paper addresses that gap. We provide a self-contained primer on causal inference for SE researchers, covering the potential outcomes framework, graphical causal models, and design-based identification strategies.
```

##### ✅ GOOD
```latex
Empirical software engineering research frequently investigates causal questions.
This disconnect between causal ambition and methodological practice mirrors a well-documented crisis in psychology and health research, but the SE community lacks an accessible, unified introduction to the causal inference toolkit.
This tutorial paper addresses that gap.
We provide a self-contained primer on causal inference for SE researchers, covering the potential outcomes framework, graphical causal models, and design-based identification strategies.
```

### Capitalization After Colons

Capitalize the first letter after a colon when it introduces a complete sentence or independent clause:
- "The central question becomes: Under what conditions can we use observed data?"

Do **not** capitalize after a colon when it introduces a list, fragment, or math expression:
- "The methods include: matching, DiD, and IV."
- "Define the effect as: $Y^1 - Y^0$."

### Tone and Register

- Use a **declarative, measured** academic tone. Write with confidence but without superlatives or enthusiasm markers ("remarkably powerful," "crucially important").
- Avoid hedging language ("it seems," "perhaps," "it could be argued"). State claims directly and qualify them with precise conditions instead.
- Prefer precise, neutral verbs: "admits a causal interpretation" over "carries a causal interpretation"; "suffices" over "does the work."
- Do not use informal phrasing ("plays out," "faith in a model"). Use register-appropriate alternatives ("applies," "plausibility of assumptions").

### Sentence and Paragraph Structure

- Sentences are short to medium length. Most begin with the subject.
- Use **em-dashes** (`---`) for parenthetical remarks, not parentheses: "When randomization is infeasible---as is common in software engineering---researchers turn to regression."
- Each `\paragraph{}` follows a **setup-formalism-interpretation** rhythm: motivate with a verbal setup, present the equation, then interpret it in words. Never let an equation stand alone without verbal explanation before and after.
- Paragraphs open with a clear topic sentence and are dense but not excessively long.

### Technical Writing Conventions

- Introduce technical terms with `\emph{}` on first use: "\emph{selection bias}," "\emph{conditional ignorability}."
- Use rhetorical questions sparingly as pedagogical devices to motivate new concepts: "Under what conditions can we estimate these quantities from observed data?"
- Weave **software engineering examples** naturally into the exposition rather than setting them apart in standalone illustrations.
- After a formal definition or estimand, provide a one-sentence practical interpretation: "The ATE answers: On average across the population, how much does treatment change outcomes?"

### Citation Style

- Use `\citet{...}` instead of writing out "XX et al.~\cite{...}" when using author names as part of the sentence (e.g., use "As \citet{DBLP:conf/sigsoft/RayPFD14} show" instead of "As Ray et al.~\cite{DBLP:conf/sigsoft/RayPFD14} show").
- Always double-check the `.bib` file and search to ensure that the citation key actually exists, especially when in doubt about the reference.

### Conciseness

- Avoid saying the same thing twice in different words. If the equation already states a result, do not restate it verbatim in prose.
- Prefer merging two short sentences into one when they share a logical thread: "Similarly, $E[Y(1) \mid D=1] = E[Y(1)]$, so the ATT equals the ATE, and the naive difference in means identifies the ATE."
- Omit meta-commentary ("It is worth noting that," "As we shall see"). Get to the point.

### Custom Commands

- **`\TODO{...}`**: Use this command for marking parts of the text that should be completed, expanded, or reviewed later. It renders the text in bold red to make it easily identifiable.
- **`\Code{...}`**: Use this command (with an uppercase C) when formatting inline code within the main text, instead of raw `\texttt{...}` or `\verb`. It ensures that the code font size looks similar to the main text font and scales properly, especially in ACM or IEEE formats.