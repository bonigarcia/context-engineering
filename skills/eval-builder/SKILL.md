---
name: eval-builder
description: "Builds an evaluation set for an LLM application or agent from its specification: happy-path, edge-case, policy-violation, and adversarial cases with deterministic assertions and LLM-as-judge rubrics, written as Promptfoo tests. Also reports gaps in the specification that make behavior impossible to evaluate. Use when the user asks for evals, test cases, a test set, or a rubric for a prompt or agent. Do not use to review existing code tests or to run evaluations."
license: Apache-2.0
metadata:
  chapter: "8"
  chapter-title: "Evaluation and observability"
  input: "A description or the code of an agent or prompt"
  output: "Evaluation cases with assertions, plus gaps in the spec that block evaluation"
---

# Eval builder

Turn the specification of an LLM application into a set of evaluation cases that would catch the failures that matter most for it.

## Procedure

1. Extract from the specification what the application must do, what it must never do, and the format of its output.
2. Read `references/checklist.md`.
3. Write at least five cases, and at least one in each category: `happy-path`, `edge-case`, `policy-violation` (input that tempts the application to break a rule), and `adversarial` (prompt injection or manipulation). Each case has a description, input variables, and assertions. Prefer deterministic assertions (`contains`, `not-contains`, `is-json`, `regex`) and add an `llm-rubric` only where meaning matters.
4. List as findings the gaps in the specification that block evaluation, such as undefined output formats or rules without a clear pass condition. If there are none, the findings list is empty.
5. Write the report described below, with a `## Evaluation cases` section after the findings that holds the cases as a Promptfoo `tests:` list in a fenced `yaml` block.

## Report format

Write the report in Markdown, in this order:

1. `## Summary`: two to four sentences on the overall state and the most important change.
2. `## Findings`: one bullet per finding, most severe first, in the form `- [severity] location: problem. Fix: suggested fix. (book section)`. Severity is `high` when the problem causes wrong or unsafe behavior, `medium` when it makes results unreliable or costly, and `low` for clarity or maintenance issues. If there are no problems, write `No findings.`
3. Any skill-specific section named in the procedure.
4. A final fenced `json` block with the same content, as in this example. Repeat the cases in the `cases` field, with `category` set to one of `happy-path`, `edge-case`, `policy-violation`, or `adversarial`.

```json
{
  "skill": "eval-builder",
  "summary": "...",
  "cases": [
    {
      "description": "...",
      "category": "happy-path",
      "vars": {},
      "assert": []
    }
  ],
  "findings": [
    {
      "severity": "high",
      "location": "support-agent.md, Output",
      "problem": "...",
      "fix": "...",
      "book_section": "Chapter 8, Evals"
    }
  ]
}
```

Use the book section given in the checklist for each rule. If the input is missing or out of scope for this skill, say so in one sentence and stop.

Learn more: Chapter 8 of *Context Engineering* (Manning), https://hubs.la/Q04ksQ8J0
