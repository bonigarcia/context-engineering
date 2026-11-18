# Memory and state checklist

Each rule has a short rationale and the book section where the idea is explained.

## Memory versus state

1. Memory holds what the agent knows (facts, preferences, past outcomes). State holds where the agent is in its work (current step, partial results, pending actions). Mixing them makes both hard to update and inspect. (Chapter 5, Memory vs state)
2. Session (short-term) memory covers the current conversation. Long-term memory covers facts that stay true across sessions. Each item has one home. (Chapter 5, Short-term memory)
3. Task progress (a booking in progress, a multi-step workflow) is stored as explicit, structured state, not inferred again from the chat history on every turn. History gets trimmed, and inferred progress gets lost with it. (Chapter 5, Categories of state)

## Writing

4. Long-term memory stores distilled facts ("prefers aisle seats", "vegetarian"), not full transcripts. Transcripts are large, noisy, and hard to search, and they may contain personal data with no purpose. (Chapter 5, Memory writing)
5. Memories are written when the user states or confirms a durable fact, with its source and date, and updated or deleted when the fact changes. (Chapter 5, Memory writing)
6. Facts the agent needs across sessions, such as stable preferences, are written to long-term memory. An agent that asks for the same preferences every time has a missing write path. (Chapter 5, Memory writing)

## Selection and compression

7. Only memories relevant to the current request are placed in the context, selected by topic, recency, or similarity. (Chapter 5, Memory selection)
8. Session memory is compressed as the conversation grows: older turns are summarized and facts still needed are kept verbatim. (Chapter 5, Memory compression)

## State management

9. State has a defined schema (fields, allowed values) and is updated by explicit operations, so it can be validated and inspected. (Chapter 5, State representation)
10. Workflow state that must survive a crash, a timeout, or a handoff to another agent is persisted with checkpoints. (Chapter 5, State persistence and checkpointing)
11. Each agent or step sees only the part of the state it needs. (Chapter 5, State selection and projection)

## Safeguards

12. Memory has retention limits, and personal data in memory follows the same rules as personal data anywhere else: purpose, consent, and deletion on request. (Chapter 5, Failure modes and safeguards)
13. Memories from untrusted content (web pages, tool outputs) are not written as facts without validation, since they can poison later sessions. (Chapter 5, Failure modes and safeguards)
