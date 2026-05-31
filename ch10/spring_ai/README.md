# Spring AI for context engineering

This chapter bucket contains a minimal Spring AI example that runs against a local Ollama server.

## Examples

- `basic_assistant/`: a tiny Spring Boot app that sends one prompt to a local Ollama chat model and prints the reply

## Run the example

1. Start Ollama and pull a small chat model:
   ```bash
   ollama serve
   ollama pull llama3.2:1b
   ```
2. Run the example:
   ```bash
   cd ch10/spring_ai/basic_assistant
   mvn spring-boot:run
   ```

The app prints one assistant response from Spring AI and then exits.
