# System prompt in Java

This folder contains Java examples for interacting with OpenAI, Anthropic, and Google Gemini models using system prompts.

## Requirements

- [Java](https://www.oracle.com/java/technologies/downloads/) 25+
- [Maven](https://maven.apache.org/) 3.9+
- Corresponding API keys are set as environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `GOOGLE_API_KEY`) 

## Examples

- `OpenAiGptSystemPrompt.java`: System prompt with OpenAI GPT models.
- `AnthropicClaudeSystemPrompt.java`: System prompt with Anthropic Claude models.
- `GoogleGeminiSystemPrompt.java`: System prompt with Google Gemini models.

## Running the examples

You can run each example using Maven:

```bash
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.OpenAiGptSystemPrompt"
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.AnthropicClaudeSystemPrompt"
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.GoogleGeminiSystemPrompt"
```
