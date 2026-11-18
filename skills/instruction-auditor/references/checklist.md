# Instruction audit checklist

Each rule has a short rationale and the book section where the idea is explained.

## Consistency

1. No two rules contradict each other, within one file or across files that load together (for example a root AGENTS.md and a nested one). When rules conflict, the model picks one unpredictably. (Chapter 2, Best practices for designing instruction artifacts)
2. Rules that override others say so explicitly, including their scope (for example "in the `legacy/` folder, use..."). (Chapter 2, Instruction artifacts in coding agents)

## Clarity

3. Every rule is concrete enough to check. "Write clean, high-quality code" cannot be verified. "Functions longer than 50 lines must be split" can. (Chapter 2, Best practices for designing instruction artifacts)
4. Rules that cannot be followed literally ("never make mistakes", "always be correct") are removed. They add tokens and no behavior. (Chapter 2, Content of the system prompt)
5. Commands are written exactly as they must be run, with the working directory when it matters. (Chapter 2, Instruction artifacts in coding agents)
6. Each rule states the reason when the reason is not obvious, so the model can apply it to cases the rule does not name. (Chapter 2, Content of the system prompt)

## Scope and size

7. The file holds durable project guidance: build and test commands, layout, conventions, and constraints. Long step-by-step procedures used only for some tasks (releases, migrations, incident handling) move to a skill that loads on demand. (Chapter 2, Agent skills)
8. Exact, repeatable checks (formatting, linting, license headers) are enforced by tools or scripts that the file names, not described in prose for the model to apply by hand. (Chapter 2, Best practices for designing instruction artifacts)
9. The file stays short. As a rule of thumb, more than about 300 lines or 4,000 tokens deserves a split into nested files or skills, since every token loads into every call. (Chapter 2, Best practices for designing instruction artifacts)
10. Information that the agent can read from the repository itself (the full dependency list, file trees that change often) is not copied into the file, since copies go stale. (Chapter 2, Best practices for designing instruction artifacts)

## Structure

11. Sections have clear headings, and related rules sit together, so the model and the humans who maintain the file can find them. (Chapter 2, Content of the system prompt)
12. The file contains no secrets, tokens, or personal data. Instruction files are versioned and often public. (Chapter 2, Best practices for designing instruction artifacts)
