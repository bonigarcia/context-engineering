# System prompt with OpenAI GPT models

This example demonstrates how to set up an [OpenAI](https://openai.com/) GPT model and send a system prompt with JavaScript.

## Requirements

* [Node.js](https://nodejs.org/)
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1.  Install dependencies:
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

When you run the script, it will send a system prompt and a user prompt to the model, which should provide a response:

```
=== With system instructions ===
User: Explain me what is context engineering in simple words
AI: Explain to me what context engineering is in simple words.

=== With only user prompt ===
User: Explain me what is context engineering in simple words
AI: Context engineering is the process of designing and organizing information or systems in a way that makes it easier for people to understand and use them in specific situations. It involves considering the environment, needs, and goals of users to create a more relevant and effective experience.

For example, if you're creating a website, context engineering would mean thinking about who will use the site, what they are looking for, and how to present the information in a way that makes sense for them. This helps ensure that users can find what they need quickly and easily, leading to a better overall experience.
```