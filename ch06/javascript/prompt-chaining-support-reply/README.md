# Prompt chaining support reply

This example demonstrates prompt chaining by splitting a support workflow into two model calls.

The first prompt extracts structured fields from a customer message. The second prompt uses that structured result to draft a concise support reply.

## Requirements

* [Node.js](https://nodejs.org/)
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1. Install dependencies:
```bash
npm install
```

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
npm start
```

## Output

When you run the script, it will print the intermediate structured extraction and the final support reply generated from that intermediate context.
