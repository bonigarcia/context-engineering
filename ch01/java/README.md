# Basic interaction with LLMs in Java

This folder contains Java examples for interacting with OpenAI, Anthropic, and Google Gemini models.

## Requirements

- [Java](https://www.oracle.com/java/technologies/downloads/) 21+
- [Maven](https://maven.apache.org/) 3.9+
- Corresponding API keys are set as environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `GEMINI_API_KEY`) 

## Examples

- `OpenAiGptBasic.java`: Basic interaction with OpenAI GPT models.
- `AnthropicClaudeBasic.java`: Basic interaction with Anthropic Claude models.
- `GoogleGeminiBasic.java`: Basic interaction with Google Gemini models.

## Running the examples

You can run each example using Maven:

```bash
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.ch01.OpenAiGptBasic"
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.ch01.AnthropicClaudeBasic"
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.ch01.GoogleGeminiBasic"
```