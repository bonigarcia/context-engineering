# Basic interaction with OpenAI GPT models

This example demonstrates how to set up an OpenAI GPT model and send a basic user prompt with Python.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```
Alternatively, create a `.env` file in the source directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

3. Run the script:
```bash
python openai-gpt-basic.py
```

## Output

When you run the script, it will send a basic user prompt to the LLM as input and the model should provide a response:

```
User: How many tokens is your context window?
AI: My context window is 32,768 tokens. This means I can process and keep track of up to 32,768 tokens of text in a single conversation or input. If you have any other questions about how this works, feel free to ask!
```
