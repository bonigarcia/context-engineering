# Basic interaction with LLMs in Java

This folder contains Java examples for interacting with OpenAI, Anthropic, Google Gemini, and local Ollama models.

## Requirements

- [Java](https://www.oracle.com/java/technologies/downloads/) 21+
- [Maven](https://maven.apache.org/) 3.9+
- Corresponding API keys are set as environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `GEMINI_API_KEY`) for cloud examples
- [Ollama](https://ollama.com/) installed locally for the local model example

## Examples

- `OpenAiGptBasic.java`: Basic interaction with OpenAI GPT models.
- `OpenAiGptStreaming.java`: Streaming responses from OpenAI GPT models.
- `AnthropicClaudeBasic.java`: Basic interaction with Anthropic Claude models.
- `AnthropicClaudeStreaming.java`: Streaming responses from Anthropic Claude models.
- `GoogleGeminiBasic.java`: Basic interaction with Google Gemini models.
- `GoogleGeminiStreaming.java`: Streaming responses from Google Gemini models.
- `OllamaLocalBasic.java`: Basic interaction with a local LLM using Ollama.
- `OllamaLocalStreaming.java`: Streaming responses from a local LLM using Ollama.

## Running the examples

You can run each example using Maven:

```bash
mvn compile exec:exec -Dexec.mainClass="io.github.bonigarcia.ce.OpenAiGptBasic"
mvn compile exec:exec -Dexec.mainClass="io.github.bonigarcia.ce.OpenAiGptStreaming"
mvn compile exec:exec -Dexec.mainClass="io.github.bonigarcia.ce.AnthropicClaudeBasic"
mvn compile exec:exec -Dexec.mainClass="io.github.bonigarcia.ce.AnthropicClaudeStreaming"
mvn compile exec:exec -Dexec.mainClass="io.github.bonigarcia.ce.GoogleGeminiBasic"
mvn compile exec:exec -Dexec.mainClass="io.github.bonigarcia.ce.GoogleGeminiStreaming"
mvn compile exec:exec -Dexec.mainClass="io.github.bonigarcia.ce.OllamaLocalBasic"
mvn compile exec:exec -Dexec.mainClass="io.github.bonigarcia.ce.OllamaLocalStreaming"
```
