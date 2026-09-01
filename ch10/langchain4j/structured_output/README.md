# Structured output with LangChain4j and Ollama

This example shows LangChain4j returning a typed Java record from a local Ollama model.

The record declares the expected shape, LangChain4j derives a JSON schema from it, and the response arrives as a validated object.

## Requirements

* [Java](https://www.oracle.com/java/technologies/downloads/) 21+
* [Maven](https://maven.apache.org/) 3.9+
* [Ollama](https://ollama.com/) installed locally
* A pulled chat model such as `llama3.2:1b`

## Steps for running this example in the shell

1. Start Ollama and pull the model:
```bash
ollama serve
ollama pull llama3.2:1b
```

2. Run the application:
```bash
mvn compile exec:java
```

## Output

```
ReleaseSummary[title=Release Readiness Check, priority=High, nextStep=Fix flaky integration tests]
```
