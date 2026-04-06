# Paper-Specific Agent Instructions

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

#### BAD
```bibtex
@article{Smith2023,
  title={Some Software Engineering Paper},
  author={Smith, John},
  year={2023}
}
```

#### GOOD (Online / Institutional Resource)
```bibtex
@online{nobelprize2021economics,
  author={{The Royal Swedish Academy of Sciences}},
  title={The {Sveriges Riksbank} Prize in Economic Sciences in Memory of {Alfred Nobel} 2021},
  year={2021},
  url={https://www.nobelprize.org/prizes/economic-sciences/2021/summary/},
  note={Accessed 2026-03-20}
}
```

#### GOOD (Non-CS Publication)
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

#### GOOD (CS Publication)
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

##### BAD
```latex
Empirical software engineering research frequently investigates causal questions. This disconnect between causal ambition and methodological practice mirrors a well-documented crisis in psychology and health research, but the SE community lacks an accessible, unified introduction to the causal inference toolkit. This tutorial paper addresses that gap. We provide a self-contained primer on causal inference for SE researchers, covering the potential outcomes framework, graphical causal models, and design-based identification strategies.
```

##### GOOD
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

## Evaluating Prior Work

When discussing, diagnosing, or reanalyzing prior studies --- both in paper text (`.tex`) and in documentation (`README.md`, plans, notebooks) --- follow these principles:

### Respectful Framing of Existing Studies

- **Never frame prior work as "wrong," "flawed," or "failing."** Prior studies made reasonable methodological choices given the conventions and tools available at the time. The purpose of this tutorial is to show how the causal inference toolkit can *improve upon* existing designs, not to criticize them.
- **Distinguish between what a study claims and how it is interpreted downstream.** Many studies (including Ray et al. 2014/2017) carefully present associational findings without claiming causation. The identification gap is a *structural feature* of the field's dominant methods, not a fault of individual researchers. When downstream papers or practitioners misinterpret associational findings as causal, the problem lies in the absence of identification infrastructure in the field, not in the original study.
- **Use constructive language.** Prefer "the cross-sectional design limits causal interpretation" over "the study fails to establish causation." Prefer "the toolkit suggests a stronger identification strategy" over "the authors should have used X." Prefer "the design can be improved by" over "the design is inadequate because."
- **Acknowledge contributions before discussing limitations.** Every study we reanalyze made a substantive contribution --- Ray et al. produced a landmark large-scale empirical analysis; Bogner & Merkel provided a useful comparison of JS and TS ecosystems. Lead with what the study accomplished before discussing how the causal toolkit offers a different lens.

### Measurement and Identification Are Orthogonal Challenges

The paper addresses **identification** --- the conditions under which observational data can bear a causal interpretation. It does **not** claim to resolve the equally important challenge of **measurement** --- whether the outcomes and treatments being measured are valid proxies for the constructs of interest (e.g., whether bug-fix commits reliably proxy for defect proneness, or whether "language" is a well-defined treatment). These are orthogonal problems:

- **Identification** asks: Given that we are measuring the right things, can our research design distinguish a causal effect from confounding? This is what the causal inference toolkit addresses.
- **Measurement** asks: Are we measuring the right things in the first place? Noisy proxies, construct validity issues, and ambiguous treatment definitions can undermine even a perfectly identified study.

Persistent empirical controversies in SE --- such as the PL vs. code quality debate --- remain unresolved partly because of identification failures (which this paper addresses) and partly because of measurement challenges (which this paper acknowledges but does not solve). When writing about the paper's contributions:
- **Never frame causal identification as a complete solution** to empirical controversies. It addresses one necessary dimension, not all of them.
- **Acknowledge measurement limitations explicitly** when discussing worked examples (e.g., the bug-fix labeling heuristic in Ray et al., the bug-fix commit ratio in Bogner & Merkel).
- **Do not imply that applying causal methods would have "resolved" a debate.** The correct framing is that causal methods would have *clarified the identification dimension* of the debate, while measurement challenges would remain.

### Ray et al. (2014/2017) Specifically

Ray et al.'s study is a central case study in this paper. The authors carefully framed their findings as associational ("a modest but significant relationship") and did not claim to establish a causal effect of programming languages on defect proneness. The misinterpretation problem documented in Section 4.2 is a *downstream* phenomenon --- it reflects the field's lack of causal inference infrastructure, not any error by the original authors. When discussing this study:
- Always acknowledge that the authors used appropriately hedged language.
- Frame the reanalysis as "applying new tools to an existing dataset to demonstrate the toolkit" rather than "correcting errors in the original study."
- The lesson is about what the *field* can learn from applying causal methods, not about what the *authors* did wrong (they did nothing wrong --- they presented associational findings as associational findings).
