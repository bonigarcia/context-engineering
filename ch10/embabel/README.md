# Embabel examples

This folder contains Kotlin examples demonstrating agent development using Embabel.

Embabel computes the plan instead of prompting for it. Every example declares actions as annotated methods whose parameter and return types state what the step consumes and produces, and a goal-oriented action planning engine searches those types for a path to the declared goal.

## Requirements

- [Java](https://www.oracle.com/java/technologies/downloads/) 21+
- [Maven](https://maven.apache.org/) 3.9+
- [Ollama](https://ollama.com/) installed locally for running model examples

Embabel 1.5.1 builds on Spring Boot 4.1 and Spring AI 2.0, so these examples use the `spring-boot-starter-parent` 4.1.1 and import the `embabel-agent-dependencies` BOM. Pinning an older Spring Boot parent leaves a mixed Spring AI classpath and the application fails to start.

Embabel plans and ranks with the model, so these examples use `llama3.1:8b` instead of the smaller models used elsewhere in this chapter. An OpenAI or Anthropic key works as well after swapping the Ollama starter for the matching provider starter.

## Examples

- `basic_agent/`: Two actions and a goal, chained by their types.
- `goal_planning/`: Two routes to the same goal, selected by action cost and replanning.
- `persona_prompt/`: Reusable instruction fragments contributed to a model call.

## Running the examples

Each example is in its own folder and contains a `README.md` with instructions on how to run it.
