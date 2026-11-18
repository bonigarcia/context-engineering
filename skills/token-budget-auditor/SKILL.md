---
name: token-budget-auditor
description: "Measures how many tokens each context source (instructions, tools, external knowledge, memory and history, user input) contributes to an agent's model calls, compares the total with a token budget, and reports where to select, compress, or isolate context. Use when the user asks why their context is so large, how to cut token cost or latency, or how much of the context window their agent uses. Do not use to review the quality of the instructions themselves (use instruction-auditor)."
license: Apache-2.0
metadata:
  chapter: "7"
  chapter-title: "Context management and orchestration"
  input: "The files and prompts that make up an agent's context"
  output: "Token count per context source against a token budget, with reduction findings"
---

# Token budget auditor

Measure what fills this agent's context, compare it with the token budget, and tell the user what to remove, compress, or move out of the main context.

## Procedure

1. Map each input file or block to a context source: `instructions` (system prompt, instruction artifacts, loaded skills), `tools` (tool definitions), `knowledge` (retrieved or stuffed documents), `memory` (conversation history, stored memories, state), or `input` (the current user message).
2. Find the token budget: use the number the user gives. Otherwise ask for it, or use 25% of the model's context window and state that assumption.
3. From the user's project root, run `python3 <this skill's directory>/scripts/count_tokens.py --budget <N> <source>=<path> ...`, with one argument per file or folder and paths relative to the project root. Copy its JSON output into the `tokens` field. If Python is not available, estimate characters divided by four per source and say so in the summary.
4. Read `references/checklist.md` and look for the patterns it lists, starting with the largest source.
5. Write the report described below, with a `## Token budget` section after the summary: a table with one row per source and the columns Source, Files, Tokens, and Share of total, followed by the total and the budget.

## Report format

Write the report in Markdown, in this order:

1. `## Summary`: two to four sentences on the overall state and the most important change.
2. `## Findings`: one bullet per finding, most severe first, in the form `- [severity] location: problem. Fix: suggested fix. (book section)`. Severity is `high` when the problem causes wrong or unsafe behavior, `medium` when it makes results unreliable or costly, and `low` for clarity or maintenance issues. If there are no problems, write `No findings.`
3. Any skill-specific section named in the procedure.
4. A final fenced `json` block with the same content, as in this example.

```json
{
  "skill": "token-budget-auditor",
  "summary": "...",
  "tokens": {
    "method": "estimate:chars/4",
    "budget": 8000,
    "sources": [],
    "total": 0,
    "over_budget": false
  },
  "findings": [
    {
      "severity": "high",
      "location": "retrieved.md",
      "problem": "...",
      "fix": "...",
      "book_section": "Chapter 7, Context selection"
    }
  ]
}
```

Use the book section given in the checklist for each rule. If the input is missing or out of scope for this skill, say so in one sentence and stop.

Learn more: Chapter 7 of *Context Engineering* (Manning), https://hubs.la/Q04ksQ8J0
