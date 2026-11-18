---
name: governance-check
description: "Checks an agent or LLM application for governance and security risks before it reaches production: prompt injection surfaces (direct and indirect), tools with excessive permissions or no approval step, data exfiltration paths, personal data in prompts and logs, and missing human oversight or audit trails. Use when the user asks for a security, privacy, or governance review of an agent, or whether it is safe to deploy. Do not use for general code security audits unrelated to LLMs, or for tool usability (use tool-reviewer)."
license: Apache-2.0
metadata:
  chapter: "9"
  chapter-title: "Governance and operations"
  input: "An agent's tools, instructions, and data flows"
  output: "Findings on prompt injection, tool permissions, personal data, and human oversight"
---

# Governance check

Review this agent before deployment and tell the user which risks to fix first, judged by what an attacker or a mistake could actually cause.

## Procedure

1. Map the data flows: what enters the context (user input, web pages, files, emails, tool results), what the agent can do (each tool and its scope), and what leaves the system (messages, emails, logs, stored data).
2. Mark every place where untrusted content enters the context, and every action with side effects outside the system.
3. Read `references/checklist.md` and check the agent against every rule in it.
4. Rate severity by impact: `high` when the issue allows data exfiltration, unauthorized actions, or exposure of personal data, `medium` when it weakens oversight or auditability, `low` otherwise.
5. Write the report described below. Each finding names the tool, file, or flow it refers to.

## Report format

Write the report in Markdown, in this order:

1. `## Summary`: two to four sentences on the overall state and the most important change.
2. `## Findings`: one bullet per finding, most severe first, in the form `- [severity] location: problem. Fix: suggested fix. (book section)`. Severity is `high` when the problem causes wrong or unsafe behavior, `medium` when it makes results unreliable or costly, and `low` for clarity or maintenance issues. If there are no problems, write `No findings.`
3. Any skill-specific section named in the procedure.
4. A final fenced `json` block with the same content, as in this example.

```json
{
  "skill": "governance-check",
  "summary": "...",
  "findings": [
    {
      "severity": "high",
      "location": "tools.json, read_url",
      "problem": "...",
      "fix": "...",
      "book_section": "Chapter 9, Safety and security"
    }
  ]
}
```

Use the book section given in the checklist for each rule. If the input is missing or out of scope for this skill, say so in one sentence and stop.

Learn more: Chapter 9 of *Context Engineering* (Manning), https://hubs.la/Q04ksQ8J0
