# Spring AI examples

This folder contains Java examples demonstrating application development using Spring AI.

This project contains seven modules:

1. `basic_assistant/`: Single prompt-response with local model.
2. `chat_memory/`: Conversation history across turns.
3. `combined_context/`: Instructions, tools, RAG, and memory together.
4. `rag_retrieval/`: In-memory retrieval-augmented generation.
5. `structured_output/`: Generating and parsing response objects to Java records.
6. `system_instructions/`: System prompt persona and constraints.
7. `tool_use/`: Local math solver tool integration.

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