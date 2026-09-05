# Evaluation with Spring AI and Ollama

This example shows the **Evaluation** cross-cutting concern — using
`RelevancyEvaluator` and `FactCheckingEvaluator` from Spring AI's
`Evaluator` API.

Both evaluators use a separate ChatClient to judge the quality of the
response against the context.

## Requirements

* Java 21+, Maven 3.9+, Ollama with `llama3.1:8b`

## Steps

```
ollama serve
ollama pull llama3.1:8b
mvn spring-boot:run
```

## Output

```
Question: How do I reset my password?
Answer: Use the self-service portal, then sign in again to confirm.
Context: Password reset: use the self-service portal, then sign in again.
---
Relevancy: PASS
```