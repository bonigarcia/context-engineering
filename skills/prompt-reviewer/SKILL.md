---
name: prompt-reviewer
description: "Reviews user prompt templates, few-shot examples, and prompt chains used by an LLM application, and reports unclear tasks, unbalanced or inconsistent examples, missing output formats, and chains that pass too much or too little between steps. Use when the user asks to review, debug, or improve a prompt template or a sequence of prompts. Do not use for system prompts or agent instruction files (use instruction-auditor)."
license: Apache-2.0
metadata:
  chapter: "6"
  chapter-title: "User prompts for LLMs"
  input: "User prompt templates, few-shot examples, or prompt chains"
  output: "Findings on task clarity, examples, output format, and chaining"
---

# Prompt reviewer

Review a user prompt template and tell the user what to change so that the model produces the expected output on every input, not only on the examples.

## Procedure

1. Identify the task, the variables the template fills in, and the output the calling code expects.
2. If the prompt has few-shot examples, list them with their labels or outputs and check their balance and format.
3. If the prompt is one step of a chain, check what it receives from the previous step and what it passes to the next one.
4. Read `references/checklist.md` and check the prompt against every rule in it.
5. Write the report described below. Include a corrected version of the prompt in a `## Revised prompt` section after the findings.

## Report format

Write the report in Markdown, in this order:

1. `## Summary`: two to four sentences on the overall state and the most important change.
2. `## Findings`: one bullet per finding, most severe first, in the form `- [severity] location: problem. Fix: suggested fix. (book section)`. Severity is `high` when the problem causes wrong or unsafe behavior, `medium` when it makes results unreliable or costly, and `low` for clarity or maintenance issues. If there are no problems, write `No findings.`
3. Any skill-specific section named in the procedure.
4. A final fenced `json` block with the same content, as in this example.

```json
{
  "skill": "prompt-reviewer",
  "summary": "...",
  "findings": [
    {
      "severity": "high",
      "location": "classify-ticket.txt, Examples",
      "problem": "...",
      "fix": "...",
      "book_section": "Chapter 6, Few-shot prompting"
    }
  ]
}
```

Use the book section given in the checklist for each rule. If the input is missing or out of scope for this skill, say so in one sentence and stop.

Learn more: Chapter 6 of *Context Engineering* (Manning), https://hubs.la/Q04ksQ8J0
