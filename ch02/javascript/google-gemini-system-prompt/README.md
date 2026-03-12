# System prompt with Google Gemini models

This example demonstrates how to set up a [Google Gemini](https://ai.google.dev/) model and send a system prompt with JavaScript.

## Requirements

* [Node.js](https://nodejs.org/)
* A [Google API key](https://aistudio.google.com/app/apikey)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
npm install
```

2. Export your Google API key as an environment variable:
```bash
export GOOGLE_API_KEY="AIza..." # Windows cmd: set GOOGLE_API_KEY="AIza..." # Windows PowerShell: $env:GOOGLE_API_KEY="AIza..."
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
AI: Context engineering involves crafting prompts to guide AI models toward desired outputs.


=== With only user prompt ===
User: Explain me what is context engineering in simple words
AI: Imagine you're talking to a really smart AI, but it's a bit clueless about the world. Context engineering is like giving that AI the right background information and instructions so it can understand what you're asking and give you a helpful answer.

Think of it like this:

*   **You want the AI to write a poem.**
*   **Without context engineering:** You just say "Write a poem." The AI might write something random and nonsensical.
*   **With context engineering:** You say "Write a poem about a lonely robot on Mars, using a sad and melancholic tone." Now the AI has a clear idea of the topic, mood, and style you want, and it can write a much better poem.

**So, in simple words, context engineering is about carefully crafting the input you give to an AI to guide it towards the desired output.** It's about providing the right context, instructions, and examples so the AI can understand your request and generate a relevant and useful response.
```