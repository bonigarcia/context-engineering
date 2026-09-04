# Context compression with Spring AI and Ollama

This example shows **Compression** — using `TokenTextSplitter` to split
content into token-bounded chunks, and `JTokkitTokenCountEstimator` to
measure token usage.

Compression in the context engineering stack is about reducing the size of
context before it enters the model. Token-aware splitting and counting are
the foundation of that.

## Requirements

* Java 21+, Maven 3.9+, Ollama with `llama3.2:3b`

## Steps

```
ollama serve
ollama pull llama3.2:3b
mvn spring-boot:run
```

## Output

```
Original text: The quarterly report shows...

---
Tokens before: 101, chunks: 1
Tokens after:  82, chunks: 2
Compression:  19 tokens removed
  Chunk 1: 57 tokens — The quarterly report shows...
  Chunk 2: 25 tokens — Capital expenditures reached...
---
Summary of first chunk: Revenue grew 15%, EMEA 45%, APAC 22% fastest...
```