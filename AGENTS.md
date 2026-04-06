# AI Agent Instructions

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

**BAD** (Title too long, no empty line, descriptive mood)
```text
Added the new user authentication module and fixed the login bug that was causing users to be logged out randomly when navigating between pages
Now the system uses JWT tokens with a 24-hour expiration instead of session cookies. I also updated the database schema to store refresh tokens.
```

**GOOD**
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
