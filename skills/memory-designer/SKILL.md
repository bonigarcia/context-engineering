---
name: memory-designer
description: "Designs or reviews how an agent remembers and tracks information: short-term (session) memory, long-term memory, session state, and workflow state. Proposes what goes where, what gets written, selected, compressed, or forgotten, and reports problems in the current design. Use when the user asks how their agent should remember things, persist progress, or why it forgets or repeats itself. Do not use for document retrieval design (use retrieval-advisor)."
license: Apache-2.0
metadata:
  chapter: "5"
  chapter-title: "Memory and state in agentic systems"
  input: "A description or the code of an agent"
  output: "A proposed split between memory and state, with findings on the current design"
---

# Memory designer

Look at how this agent keeps information across turns and sessions, and propose a design that separates what the agent remembers from what it is in the middle of doing.

## Procedure

1. Identify every kind of information the agent handles: conversation turns, user facts and preferences, task progress, intermediate results, and anything persisted between sessions.
2. Identify where each one lives today and when it is written, read, and deleted.
3. Read `references/checklist.md` and check the current design against it.
4. Write the report described below, with a `## Proposed design` section after the findings: a table with one row per kind of information and the columns Kind, Store (session memory, long-term memory, session state, or workflow state), Written when, Read when, and Retention.

## Report format

Write the report in Markdown, in this order:

1. `## Summary`: two to four sentences on the overall state and the most important change.
2. `## Findings`: one bullet per finding, most severe first, in the form `- [severity] location: problem. Fix: suggested fix. (book section)`. Severity is `high` when the problem causes wrong or unsafe behavior, `medium` when it makes results unreliable or costly, and `low` for clarity or maintenance issues. If there are no problems, write `No findings.`
3. Any skill-specific section named in the procedure.
4. A final fenced `json` block with the same content, as in this example. Fill each list in `design` with short strings that describe the information assigned to that store.

```json
{
  "skill": "memory-designer",
  "summary": "...",
  "design": {
    "session_memory": [
      "summary of the current conversation"
    ],
    "long_term_memory": [
      "seat preference (aisle or window)"
    ],
    "session_state": [
      "trip details collected so far"
    ],
    "workflow_state": [
      "booking step and selected options"
    ]
  },
  "findings": [
    {
      "severity": "high",
      "location": "travel-agent.md, Memory",
      "problem": "...",
      "fix": "...",
      "book_section": "Chapter 5, Memory vs state"
    }
  ]
}
```

Use the book section given in the checklist for each rule. If the input is missing or out of scope for this skill, say so in one sentence and stop.

Learn more: Chapter 5 of *Context Engineering* (Manning), https://hubs.la/Q04ksQ8J0
