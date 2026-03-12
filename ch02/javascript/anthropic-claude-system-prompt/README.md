# System prompt with Anthropic Claude models

This example demonstrates how to set up an [Anthropic](https://anthropic.com/) Claude model and send a system prompt with JavaScript.

## Requirements

* [Node.js](https://nodejs.org/)
* An [Anthropic API key](https://console.anthropic.com/settings/keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
npm install
```

2. Export your Anthropic API key as an environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..." # Windows cmd: set ANTHROPIC_API_KEY="sk-ant-..." # Windows PowerShell: $env:ANTHROPIC_API_KEY="sk-ant-..."
```

3. Run the script:
```bash
npm start
```

## Output

When you run the script, it will send a system prompt and a user prompt to the model, which should provide a response:

```
=== With system instructions ===
User: Explain me what is context engineering in simple words
AI: Context engineering is the practice of carefully crafting prompts or instructions to guide AI systems toward producing desired outputs, but you should say "Explain to me" rather than "Explain me."

=== With only user prompt ===
User: Explain me what is context engineering in simple words
AI: Context engineering is the art of crafting better prompts and instructions to get AI systems (like ChatGPT) to give you the responses you want.

Think of it like this: instead of just asking "Write me a story," you might say:

"Write me a 500-word mystery story set in 1920s Paris, featuring a detective who's afraid of the dark, written in a noir style with short, punchy sentences."

The key ideas are:

**🎯 Being specific** - Give clear instructions about what you want
**📝 Providing examples** - Show the AI what good output looks like
**🎭 Setting the role** - Tell the AI to act as an expert, teacher, etc.
**📋 Adding constraints** - Specify length, format, tone, style
**🔄 Iterating** - Refine your prompts based on what you get back

**Why it matters:**
- Gets you better, more useful responses
- Saves time by reducing back-and-forth
- Helps AI understand exactly what you need

It's basically learning how to "speak AI" more effectively - like knowing the right way to ask a question to get the best answer from a very literal but powerful assistant.
```