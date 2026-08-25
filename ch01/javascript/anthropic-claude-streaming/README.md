# Streaming responses from Anthropic Claude models

This example demonstrates how to stream the response of an [Anthropic](https://www.anthropic.com/) model with JavaScript. Instead of waiting for the complete answer, the script prints each fragment as the model produces it and reports the time to first token.

## Requirements

* [Node.js](https://nodejs.org/) 18+
* An [Anthropic API key](https://platform.claude.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
npm install
```

2. Export your API key as an environment variable:
```bash
export ANTHROPIC_API_KEY="..." # Windows cmd: set ANTHROPIC_API_KEY="..." # Windows PowerShell: $env:ANTHROPIC_API_KEY="..."
```

3. Run the script:
```bash
npm start
```

## Output

When you run the script, it sends a user prompt to a Claude model (`claude-haiku-4-5`) and prints the answer as it is generated. Once the stream ends, it prints the model identifier, the time to first token, the total latency, and the token counts. The example uses the `messages.stream()` helper, which accumulates the streamed events so that `finalMessage()` resolves with the complete message together with its usage.
