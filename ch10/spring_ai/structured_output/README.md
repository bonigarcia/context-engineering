# Structured output with Spring AI and Ollama

This example shows Spring AI returning a typed Java record from a local Ollama model.

It asks for a tiny release summary and maps the JSON output into a record.

## Requirements

- Java 21+
- Maven 3.9+
- Ollama running locally on `http://localhost:11434`
- A pulled chat model such as `llama3.2:1b`

## Run

```bash
ollama serve
ollama pull llama3.2:1b
cd ch10/spring_ai/structured_output
mvn spring-boot:run
```

## Output

The app prints a typed summary built from the model response.
