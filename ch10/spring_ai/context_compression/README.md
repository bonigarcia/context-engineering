# Context compression with Spring AI and Ollama

This example shows **Compression** — using `TokenTextSplitter` to split
content into token-bounded chunks, and `JTokkitTokenCountEstimator` to
measure token usage.

In the context engineering stack, compression is about partitioning content
into token-bounded chunks so each fits within the model's context window.

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
Original text (126 tokens, 2 chunks):
  Chunk 1: 96 tokens — The quarterly report shows revenue growth of 15%... net profit margin improved to 18.5%...
  Chunk 2: 30 tokens — Capital expenditures reached $3.2M for infrastructure upgrades...
  (Total: 2 chunks of ≤100 tokens)

Summary of first chunk: Revenue grew 15%, APAC fastest at 22%, net profit margin 18.5%...
```