# Tool use with Spring AI and Ollama

This example shows Spring AI tool calling against a local Ollama model.

It exposes one tiny math tool, asks the model a question that needs it, and prints the result.

## Requirements

- Java 21+
- Maven 3.9+
- Ollama running locally on `http://localhost:11434`
- A pulled chat model such as `llama3.2:1b`

## Run

```bash
ollama serve
ollama pull llama3.2:1b
cd ch10/spring_ai/tool_use
mvn spring-boot:run
```

## Output

The app prints the answer after Spring AI calls the local tool.
