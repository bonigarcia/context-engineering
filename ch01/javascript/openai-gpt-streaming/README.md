# Streaming responses from OpenAI GPT models

This example demonstrates how to stream the response of an [OpenAI](https://openai.com/) model with JavaScript. Instead of waiting for the complete answer, the script prints each fragment as the model produces it and reports the time to first token.

## Requirements

* [Node.js](https://nodejs.org/) 18+
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
npm install
```

2. Export your API key as an environment variable:
```bash
export OPENAI_API_KEY="..." # Windows cmd: set OPENAI_API_KEY="..." # Windows PowerShell: $env:OPENAI_API_KEY="..."
```

3. Run the script:
```bash
npm start
```

## Output

When you run the script, it sends a user prompt to a GPT model (`gpt-4o-mini`) and prints the answer as it is generated. Once the stream ends, it prints the model identifier, the time to first token, the total latency, and the token counts. Under streaming, the OpenAI Responses API delivers token usage on the final `response.completed` event, so the counts are only available once the stream ends.
