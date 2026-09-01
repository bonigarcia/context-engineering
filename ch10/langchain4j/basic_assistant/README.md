# Basic assistant with LangChain4j and Ollama

This example shows the smallest LangChain4j AI service backed by a local Ollama model.

The `Assistant` interface carries the system instruction as an annotation, and LangChain4j generates the implementation at runtime.

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
LangChain4j is a Java library that lets you build applications on top of large language models.
```
