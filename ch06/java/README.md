# Prompting examples in Java

This folder contains Java examples for few-shot prompting and prompt chaining.

## Requirements

- [Java](https://www.oracle.com/java/technologies/downloads/) 21+
- [Maven](https://maven.apache.org/) 3.9+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Examples

- `FewShotTicketNormalizer.java`: Normalize an unstructured bug report into a support ticket schema.
- `PromptChainingSupportReply.java`: Extract structured context first, then draft a support reply.

## Running the examples

You can run each example using Maven:

```bash
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.FewShotTicketNormalizer"
mvn compile exec:java -Dexec.mainClass="io.github.bonigarcia.ce.PromptChainingSupportReply"
```
