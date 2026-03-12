# System prompt with OpenAI GPT models

This example demonstrates how to set up an [OpenAI](https://openai.com/) GPT model and send a system prompt with Python.

## Requirements

* [Python](https://www.python.org/) 3.6+
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python openai-gpt-system-prompt.py
```

## Output

When you run the script, it will send a system prompt and a user prompt to the model, which should provide a response:

```
=== With system instructions ===
User query: Explain me what is context engineering in simple words
Response: Explain to me what context engineering is in simple words.

=== With only user prompt ===
User query: Explain me what is context engineering in simple words
Response: Context engineering is the process of designing and organizing information or systems in a way that makes it easier for people to understand and use them in specific situations. It involves considering the environment, background, and needs of users to create a more relevant and effective experience.

For example, if you're creating a website, context engineering would mean thinking about who will use the site, what they need to find, and how they will interact with it, so that everything is clear and helpful for them. Essentially, it's about making sure that the right information is available at the right time and place.
```