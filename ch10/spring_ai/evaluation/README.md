# Evaluation with Spring AI and Ollama

This example shows the **Evaluation** cross-cutting concern — using an
LLM-as-judge to score answer quality via structured output.

A second ChatClient (the judge) receives a question, answer, and context,
and returns a typed record with numeric scores for relevance,
correctness, and completeness.

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
Question: How do I reset my password?
Answer: Use the self-service portal.
Context: Password reset: use the self-service portal, then sign in again.
---
Evaluation:
  relevance:    3/10
  correctness:  6/10
  completeness: 5/10
  notes: Answer is missing a crucial step: signing in again after using the self-service portal.
```