# Persona prompts with Embabel and Ollama

This example shows instructions kept outside the prompt string.

The `TechnicalEditor` persona is a prompt contributor, a reusable fragment that Embabel adds to any model call that asks for it. The review action supplies only the task text, and the behavioral guidance comes from the contributor.

## Requirements

* [Java](https://www.oracle.com/java/technologies/downloads/) 21+
* [Maven](https://maven.apache.org/) 3.9+
* [Ollama](https://ollama.com/) installed locally
* A pulled chat model such as `llama3.1:8b`

## Steps for running this example in the shell

1. Start Ollama and pull the chat model:
```bash
ollama serve
ollama pull llama3.1:8b
```

2. Run the application:
```bash
mvn spring-boot:run
```

## Output

```
DRAFT
A context window is a fixed token budget shared by instructions, retrieved passages, tool results, and the reply...

REVIEW
The paragraph states the budget idea clearly and gives concrete consumers of the budget. Replace the closing claim with a measurable statement about token counts.
```
