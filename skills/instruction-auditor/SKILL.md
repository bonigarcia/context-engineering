---
name: instruction-auditor
description: "Audits a system prompt or an instruction artifact (AGENTS.md, CLAUDE.md, GEMINI.md, .cursor/rules, copilot-instructions.md) and reports contradictions, vague or unenforceable rules, excessive size, and procedures that belong in a skill or a tool. Use when the user asks to review, audit, shorten, or improve agent instructions or a system prompt. Do not use for SKILL.md files (use skill-reviewer) or for user prompt templates (use prompt-reviewer)."
license: Apache-2.0
metadata:
  chapter: "2"
  chapter-title: "Instructions for AI agents"
  input: "A system prompt or an instruction artifact such as AGENTS.md or CLAUDE.md"
  output: "Findings on contradictions, vague rules, size, and misplaced procedures"
---

# Instruction auditor

Audit one set of agent instructions and tell the user what to change so that the agent follows them consistently and spends fewer tokens on them.

## Procedure

1. Read the whole artifact. If several instruction files apply to the same agent (for example a root AGENTS.md and a nested one), read all of them and treat them as one set, noting which file each rule comes from.
2. Estimate the size: count lines, and estimate tokens as characters divided by four. Record both in the `size` field.
3. Read `references/checklist.md` and check the instructions against every rule in it.
4. For each contradiction, quote both rules and their locations. For each vague rule, propose a concrete, checkable replacement.
5. Write the report described below. Report only problems you can point to. Do not report sections that are already concrete and correct.

## Report format

Write the report in Markdown, in this order:

1. `## Summary`: two to four sentences on the overall state and the most important change.
2. `## Findings`: one bullet per finding, most severe first, in the form `- [severity] location: problem. Fix: suggested fix. (book section)`. Severity is `high` when the problem causes wrong or unsafe behavior, `medium` when it makes results unreliable or costly, and `low` for clarity or maintenance issues. If there are no problems, write `No findings.`
3. Any skill-specific section named in the procedure.
4. A final fenced `json` block with the same content, as in this example.

```json
{
  "skill": "instruction-auditor",
  "summary": "...",
  "size": {
    "lines": 0,
    "tokens_estimate": 0
  },
  "findings": [
    {
      "severity": "high",
      "location": "AGENTS.md, Code style",
      "problem": "...",
      "fix": "...",
      "book_section": "Chapter 2, Best practices for designing instruction artifacts"
    }
  ]
}
```

Use the book section given in the checklist for each rule. If the input is missing or out of scope for this skill, say so in one sentence and stop.

Learn more: Chapter 2 of *Context Engineering* (Manning), https://hubs.la/Q04ksQ8J0
