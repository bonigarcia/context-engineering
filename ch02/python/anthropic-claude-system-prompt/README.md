# System prompt with Anthropic Claude models

This example demonstrates how to set up an [Anthropic](https://anthropic.com/) Claude model and send a system prompt with Python.

## Requirements

* [Python](https://www.python.org/) 3.6+
* An [Anthropic API key](https://console.anthropic.com/settings/keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Export your Anthropic API key as an environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..." # Windows cmd: set ANTHROPIC_API_KEY="sk-ant-..." # Windows PowerShell: $env:ANTHROPIC_API_KEY="sk-ant-..."
```

3. Run the script:
```bash
python anthropic-claude-system-prompt.py
```

## Output

When you run the script, it will send a system prompt and a user prompt to the model, which should provide a response:

```
=== With system instructions ===
User query: Explain me what is context engineering in simple words
Response: **Correction:** "Explain *to* me what context engineering is in simple words."

Context engineering is the practice of carefully crafting the instructions and background information you give to an AI system to get the best possible responses for your specific needs.

=== With only user prompt ===
User query: Explain me what is context engineering in simple words
Response: Context engineering is the art of crafting better prompts and instructions to get AI systems (like ChatGPT) to give you the responses you want.

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
