# Tool use with LangChain4j and Ollama

This example shows LangChain4j tool calling against a local Ollama model.

A plain Java method annotated with `@Tool` becomes callable by the model, and LangChain4j runs the tool loop on behalf of the AI service. Small models call tools unreliably, so a larger model such as `llama3.2` gives more consistent results.

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
42
```
