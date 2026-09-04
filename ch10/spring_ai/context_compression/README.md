# Context compression with Spring AI and Ollama

This example demonstrates **Compression** from the context management layer.
The system instruction asks the model to compress conversation history into
a short summary before each response, preserving key facts while keeping the
raw context window manageable.

This models the summarization-based compression pattern: instead of keeping
every raw message, the model maintains a compressed representation of past
interactions.

## Requirements

* Java 21+, Maven 3.9+, Ollama with `llama3.2:3b`

## Steps

```
ollama serve
ollama pull llama3.2:3b
mvn spring-boot:run
```

## Output

The model recalls details from early turns because the system-level
compression instruction keeps key facts alive.

```
User: Hi, my name is Alice and I work in finance
Model: Note to self: Alice, works in finance. Hello Alice! How can I help you today?

User: I need help with the quarterly report
Model: Summary: Alice in finance needs help with the quarterly report.
I'd be happy to assist you with the quarterly report!

User: The pivot table won't refresh
Model: Summary: Alice (finance) has a quarterly report issue. The pivot table won't refresh.
Let's troubleshoot that pivot table. Have you checked the data source range?

User: Actually I think it's a permissions thing
Model: Summary: Alice (finance) is working on a quarterly report. Pivot table refresh issue may be permissions-related.
Since you're in finance, check if your access to the data folder was recently changed.

User: What was my first question and what department am I in?
Model: Summary: Alice in finance had a pivot table refresh issue with her quarterly report due to permissions.
Your first question was about help with the quarterly report, and you work in finance.
```