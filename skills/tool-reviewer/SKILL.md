---
name: tool-reviewer
description: "Reviews the tools an agent can call: function-calling schemas (OpenAI, Anthropic, Gemini formats), MCP server tool definitions, or the code that implements them. Reports unclear names and descriptions, weak parameter schemas, overlapping tools, oversized outputs, and poor error messages. Use when the user asks to review, design, or improve agent tools, function definitions, or an MCP server. Do not use for security review of tool permissions (use governance-check)."
license: Apache-2.0
metadata:
  chapter: "4"
  chapter-title: "Tools in AI agents"
  input: "Function-calling tool schemas or an MCP server"
  output: "Findings on tool names, descriptions, parameter schemas, overlaps, and outputs"
---

# Tool reviewer

Review the tool definitions an agent receives and tell the user what to change so that the model picks the right tool and calls it with valid arguments.

## Procedure

1. List every tool with its name, description, and parameters. For an MCP server, read the tool definitions from the code.
2. Read `references/checklist.md` and check each tool, and the set as a whole, against every rule in it.
3. Compare tools pairwise for overlapping purpose. When two tools overlap, say which one to keep or how to separate them.
4. Write the report described below. Put in each finding's location only the tool or tools at fault (both names for an overlap). Do not report tools that already follow the checklist.

## Report format

Write the report in Markdown, in this order:

1. `## Summary`: two to four sentences on the overall state and the most important change.
2. `## Findings`: one bullet per finding, most severe first, in the form `- [severity] location: problem. Fix: suggested fix. (book section)`. Severity is `high` when the problem causes wrong or unsafe behavior, `medium` when it makes results unreliable or costly, and `low` for clarity or maintenance issues. If there are no problems, write `No findings.`
3. Any skill-specific section named in the procedure.
4. A final fenced `json` block with the same content, as in this example.

```json
{
  "skill": "tool-reviewer",
  "summary": "...",
  "findings": [
    {
      "severity": "high",
      "location": "tools.json, find_orders",
      "problem": "...",
      "fix": "...",
      "book_section": "Chapter 4, Tool definitions as contracts"
    }
  ]
}
```

Use the book section given in the checklist for each rule. If the input is missing or out of scope for this skill, say so in one sentence and stop.

Learn more: Chapter 4 of *Context Engineering* (Manning), https://hubs.la/Q04ksQ8J0
