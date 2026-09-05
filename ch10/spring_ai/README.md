# Spring AI examples

This folder contains Java examples demonstrating application development using Spring AI.

This project contains 13 modules:

1. `basic_assistant/`: Single prompt-response with local model.
2. `chat_memory/`: Conversation history across turns.
3. `combined_context/`: Instructions, tools, RAG, and memory together.
4. `context_compression/`: Token-aware text splitting and compression.
5. `evaluation/`: Fact-checking and relevancy evaluation via Spring AI's Evaluator API.
6. `observability/`: Micrometer metrics for AI call telemetry.
7. `rag_retrieval/`: In-memory retrieval-augmented generation.
8. `route_to_specialist/`: Multi-agent routing via supervisor tool dispatch.
9. `safe_guard/`: Content filtering governance with SafeGuardAdvisor.
10. `stateful_ticket/`: Session-scoped ticket state across turns.
11. `streaming/`: Token-by-token streaming response.
12. `structured_output/`: Generating and parsing response objects to Java records.
13. `system_instructions/`: System prompt persona and constraints.
14. `tool_use/`: Local math solver tool integration.

## Requirements

- [Java](https://www.oracle.com/java/technologies/downloads/) 21+
- [Maven](https://maven.apache.org/) 3.9+ (for Maven) or [Gradle](https://gradle.org/) 9.7+ (for Gradle)
- [Ollama](https://ollama.com/) installed locally for running model examples

## Building and running

This project supports both Maven and Gradle.

### Using Maven

From the root folder, build all modules at once:

```bash
mvn compile
```

To run a specific module:

```bash
mvn spring-boot:run -pl basic_assistant
```

Replace `basic_assistant` with any module name from the list above.

### Using Gradle

From the root folder, build all modules at once:

```bash
./gradlew build
```

To run a specific module:

```bash
./gradlew :basic_assistant:bootRun
```

Replace `basic_assistant` with any module name from the list above.

### Running a single module independently

Each module folder is self-contained. You can also enter any module folder and run it directly:

```bash
cd basic_assistant
mvn spring-boot:run
```

Or with Gradle:

```bash
cd basic_assistant
../gradlew bootRun
```

Each module has a `README.md` with example output.