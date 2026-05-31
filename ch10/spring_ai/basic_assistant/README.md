# Basic assistant with Spring AI and Ollama

This example shows the smallest faithful Spring AI setup for a local Ollama model.

It boots a Spring application, builds a `ChatClient` from the auto-configured `ChatModel`, sends one prompt, and prints the result.

## Requirements

- Java 21+
- Maven 3.9+
- Ollama running locally on `http://localhost:11434`
- A pulled chat model such as `llama3.2:1b`

## Run

```bash
ollama serve
ollama pull llama3.2:1b
cd ch10/spring_ai/basic_assistant
mvn spring-boot:run
```

## Output

The app prints a single response from the local model and exits.
