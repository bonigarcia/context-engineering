# Basic interaction with LLMs in Java

This folder contains Java examples for interacting with OpenAI, Anthropic, Google Gemini, and local Ollama models.

## Requirements

- [Java](https://www.oracle.com/java/technologies/downloads/) 21+
- [Maven](https://maven.apache.org/) 3.9+
- Corresponding API keys are set as environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `GEMINI_API_KEY`) for cloud examples
- [Ollama](https://ollama.com/) installed locally for the local model example

## Examples

- `OpenAiGptBasic.java`: Basic interaction with OpenAI GPT models.
- `AnthropicClaudeBasic.java`: Basic interaction with Anthropic Claude models.
- `GoogleGeminiBasic.java`: Basic interaction with Google Gemini models.
- `OllamaLocalBasic.java`: Basic interaction with a local LLM using Ollama.

## Running the examples

You can run each example using Maven:

```bash
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.OpenAiGptBasic"
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.AnthropicClaudeBasic"
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.GoogleGeminiBasic"
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.OllamaLocalBasic"
```
