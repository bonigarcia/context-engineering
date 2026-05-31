# Spring AI

This chapter bucket contains four minimal Spring AI examples that run against a local Ollama server.

## Examples

- `basic_assistant/`: a tiny Spring Boot app that sends one prompt to a local Ollama chat model and prints the reply
- `tool_use/`: a one-shot tool-calling demo with a local math helper
- `rag_retrieval/`: a small retrieval example backed by a local in-memory vector store
- `structured_output/`: a typed output example that returns a Java record

## Run the example

1. Start Ollama and pull a small chat model:
   ```bash
   ollama serve
   ollama pull llama3.2:1b
   ```
2. Run one of the examples:
    ```bash
    cd ch10/spring_ai/<example>
    mvn spring-boot:run
    ```

Each app prints one Spring AI response and then exits.
