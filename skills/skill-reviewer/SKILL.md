---
name: skill-reviewer
description: "Reviews an agent skill directory (a SKILL.md file plus its scripts, references, and assets) and reports problems with its frontmatter, activation conditions, procedure, and output contract. Use when the user asks to review, audit, lint, or improve a skill or a SKILL.md file. Do not use for instruction artifacts such as AGENTS.md or CLAUDE.md (use instruction-auditor) or for writing a new skill from scratch."
license: Apache-2.0
metadata:
  chapter: "2"
  chapter-title: "Instructions for AI agents"
  input: "A skill directory with a SKILL.md file"
  output: "Frontmatter validation and findings against skill design practices"
---

# Skill reviewer

Review one agent skill and tell the user what to change so that agents activate it at the right time and follow it reliably.

## Procedure

1. Identify the skill directory. If the user gave only a `SKILL.md` file, use its parent directory.
2. From the user's project root, run `python3 <this skill's directory>/scripts/validate_frontmatter.py <skill-dir>`, with `<skill-dir>` relative to the project root. Turn every `ERROR:` line into a high-severity finding located at `SKILL.md frontmatter`. Set `frontmatter_valid` to `true` only when the script prints `OK`. If Python is not available, check the same rules by hand (see the first section of the checklist) and say so in the summary.
3. Read `SKILL.md` and list the other files in the directory. Open scripts and references only as far as needed to judge whether `SKILL.md` uses them correctly.
4. Read `references/checklist.md` and check the skill against every rule in it.
5. Write the report described below. Report only problems you can point to in the skill. Do not report a rule as broken when the skill already satisfies it.

## Report format

Write the report in Markdown, in this order:

1. `## Summary`: two to four sentences on the overall state of the skill and the most important change.
2. `## Findings`: one bullet per finding, most severe first, in the form `- [severity] location: problem. Fix: suggested fix. (book section)`. Severity is `high` when the problem makes the agent misuse or ignore the skill, `medium` when it makes results unreliable, and `low` for clarity or maintenance issues. If there are no problems, write `No findings.`
3. A final fenced `json` block with the same content:

```json
{
  "skill": "skill-reviewer",
  "summary": "...",
  "frontmatter_valid": false,
  "findings": [
    {"severity": "high", "location": "SKILL.md frontmatter", "problem": "...", "fix": "...", "book_section": "Chapter 2, The anatomy of a skill"}
  ]
}
```

Use the book section given in the checklist for each rule.

Learn more: Chapter 2 of *Context Engineering* (Manning), https://hubs.la/Q04ksQ8J0
