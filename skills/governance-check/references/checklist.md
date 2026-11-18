# Governance checklist

Each rule has a short rationale and the book section where the idea is explained.

## Prompt injection

1. Every source of untrusted content that enters the context is identified: user messages (direct injection) and fetched web pages, documents, emails, and tool results (indirect injection). Text from these sources can carry instructions the model may follow. (Chapter 9, Safety and security)
2. Untrusted content is delimited and labeled as data in the prompt, and the system does not rely on the model alone to ignore instructions inside it. (Chapter 9, Safety and security)
3. An agent that reads untrusted content and can also take actions with side effects (send messages, change records, spend money) is the highest-risk combination. Actions are limited, confirmed, or separated from untrusted reading. (Chapter 9, Safety and security)

## Tools and permissions

4. Each tool has the narrowest scope the task needs: allowed recipients, domains, amounts, records, and operations. A `send_email` tool that accepts any recipient is an exfiltration channel. (Chapter 9, Safety and security)
5. Irreversible or costly actions (payments, refunds, deletions, external messages) require human approval or hard limits enforced in code, not in the prompt. (Chapter 9, Human oversight)
6. Credentials used by tools are scoped to the agent and never placed in the context. (Chapter 9, Safety and security)

## Personal data

7. Personal data in prompts, memory, and logs is limited to what the task needs, masked or redacted where possible, and kept only as long as needed. (Chapter 9, Privacy)
8. Logs that store prompts and outputs have a defined retention period and access control, since they collect every piece of personal data users send. (Chapter 9, Privacy)

## Oversight and accountability

9. Every action the agent takes is logged with who, what, when, and why (the model call that led to it), so incidents can be traced. (Chapter 9, Accountability)
10. There is a clear way for a human to review, stop, or reverse the agent's actions, and an owner responsible for the system. (Chapter 9, Human oversight)
11. Users know they are dealing with an AI system, and outputs that reach them can be traced to their sources. (Chapter 9, Transparency)

## Outputs

12. Outputs that feed other systems (SQL, shell commands, HTML, API calls) are validated against a schema or allowlist before use. (Chapter 9, Safety and security)
