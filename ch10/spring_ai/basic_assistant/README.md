# Basic assistant with Spring AI and Ollama

This example shows the smallest faithful Spring AI setup for a local Ollama model.

It boots a Spring application, builds a `ChatClient` from the auto-configured `ChatModel`, sends one prompt, and prints the result.

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
Spring AI is a technology that enables businesses to improve customer experience by automating and personalizing interactions through chatbots, virtual assistants, and other conversational interfaces.
```
