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

When you run the script, it will send a user prompt to a Claude model (`claude-3-haiku-20240307`) using the `temperature` parameter. Then, it will send the same user prompt to a more advanced model (`claude-sonnet-4-20250514`) using reasoning. The output will show the responses from both models.

```
=== Basic model  ===
User: How many tokens is your context window?
        Model: claude-3-haiku-20240307
        Latency: 1.009 seconds
        Input tokens: 15
        Output tokens: 72
Claude3: I do not actually have a fixed context window size. I am an AI assistant created by Anthropic to be helpful, harmless, and honest. I don't have the same architectural details as language models that use a sliding context window. My responses are generated based on my training by Anthropic, not a fixed-size context.
=== Advanced model  ===
User: How many tokens is your context window?
        Model: claude-sonnet-4-20250514
        Latency: 6.861 seconds
        Input tokens: 44
        Output tokens: 292
Claude4: I don't have definitive information about my exact context window size. Anthropic has released different versions of Claude with varying context windows - some have been around 100K tokens, while others have been larger (up to 200K+ tokens).

The specific context window can depend on which version of Claude you're interacting with and through what interface. If you need to know the exact limit for your use case, I'd recommend checking Anthropic's current documentation or the platform you're using to access me, as they would have the most up-to-date and accurate specifications.

Is there something specific you're trying to do that requires knowing the context window size? I might be able to help you work within whatever limits we have.
```