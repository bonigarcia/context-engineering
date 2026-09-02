# Basic interaction with Anthropic Claude models

This example demonstrates how to set up an [Anthropic Claude](https://www.anthropic.com/) model and send a basic user prompt with JavaScript.

## Requirements

* [Node.js](https://nodejs.org/)
* An [Anthropic API key](https://platform.claude.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
npm install
```

2. Export your Anthropic API key as an environment variable:
```bash
export ANTHROPIC_API_KEY="sk-..." # Windows cmd: set ANTHROPIC_API_KEY="sk-..." # Windows PowerShell: $env:ANTHROPIC_API_KEY="sk-..."
```

3. Run the script:
```bash
npm start
```

## Output

When you run the script, it will send a user prompt to a Claude model (`claude-haiku-4-5-20251001`). Then, it will send the same user prompt to a more advanced model (`claude-sonnet-4-6`) using extended thinking. The output will show the responses from both models.
The transcript below was captured with earlier releases of these models. Model identifiers, latency, token counts, and wording will differ on each run.


```
=== Basic model  ===
User: How many tokens are in your context window?
        Model: claude-haiku-4-5-20251001
        Latency: 1.297 seconds
        Input tokens: 16
        Output tokens: 48
Claude Haiku: I have a context window of 128,000 tokens. This means I can process and work with up to 128,000 tokens of text in a single conversation, including both the conversation history and my responses.
=== Advanced model  ===
User: How many tokens are in your context window?
        Model: claude-sonnet-4-6
        Latency: 3.788 seconds
        Input tokens: 45
        Output tokens: 133
Claude Sonnet: I don't have precise, reliable information about my exact context window size to share with confidence. Anthropic hasn't always made exact technical specifications publicly clear through my own knowledge.

What I can say:
- My context window is substantial, allowing for long conversations
- For the most accurate and current specs, I'd recommend checking **Anthropic's official documentation** at anthropic.com or the API documentation

Is there something specific you're trying to accomplish where context window size matters? I might be able to help more practically that way.
```