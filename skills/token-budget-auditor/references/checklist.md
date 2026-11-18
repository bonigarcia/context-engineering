# Token budget checklist

Each rule has a short rationale and the book section where the idea is explained.

## Budget

1. Every model call has a token budget: the share of the context window the system allows itself, set by cost per token and latency targets, below the model's hard context window limit. Measure against the budget, not against the window. (Chapter 7, Context management)
2. A large context also spends the attention budget: relevant information buried among irrelevant tokens is used less reliably, even when the total fits. (Chapter 7, Context management)

## Selection

3. Retrieved or stuffed content contains no duplicates. Identical or near-identical chunks repeat tokens and add no information. Deduplicate before assembly. (Chapter 7, Context selection)
4. Only tools relevant to the current task are loaded. A long tool list costs tokens on every call and lowers selection accuracy. Group tools and load them on demand. (Chapter 7, Context selection)
5. Instructions that apply only to some tasks are loaded only for those tasks, for example as skills. (Chapter 7, Context selection)

## Compression

6. Conversation history is not passed in full forever. Older turns are summarized or trimmed, and only facts still needed stay verbatim. (Chapter 7, Context compression)
7. Long tool outputs and documents are reduced to the parts the task needs, by extraction, summarization, or truncation with a pointer to the full content. (Chapter 7, Context compression)
8. Instructions are free of repetition. The same rule stated in several sections costs tokens each time. (Chapter 7, Context compression)

## Writing and isolation

9. Information that must survive but is not needed on every call is written outside the context (files, memory, state) and read back when needed. (Chapter 7, Context writing)
10. Subtasks that need large amounts of context (searching a codebase, reading long documents) run in a separate agent or call, which returns only a short result to the main context. (Chapter 7, Context isolation)

## Stability

11. Stable content (system prompt, tool definitions) comes first and changes rarely, so provider prompt caching can reuse it across calls. (Chapter 7, Context management)
