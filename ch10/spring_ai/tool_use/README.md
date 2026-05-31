# Tool use with Spring AI and Ollama

This example shows Spring AI tool calling against a local Ollama model.

It exposes one tiny math tool, asks the model a question that needs it, and prints the result.

## Requirements

* [Java](https://www.oracle.com/java/technologies/downloads/) 21+
* [Maven](https://maven.apache.org/) 3.9+
* [Ollama](https://ollama.com/) installed locally
* A pulled chat model such as `llama3.2:1b`

## Steps for running this example in the shell

1. Start Ollama and pull the chat model:
```bash
ollama serve
ollama pull llama3.2:1b
```

2. Run the application:
```bash
mvn spring-boot:run
```

## Output

```
{"operator":"plus", "parameters": {"left": "12", "right": "30"}}
```
