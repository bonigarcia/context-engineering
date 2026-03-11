# Basic interaction with Google Gemini models

This example demonstrates how to set up a [Google Gemini](https://gemini.google.com/) model and send a basic user prompt with Python.

## Requirements

* [Python](https://www.python.org/) 3.6+
* A [Gemini key](https://aistudio.google.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Export your Gemini API key as an environment variable:
```bash
export GEMINI_API_KEY="..." # Windows cmd: set GEMINI_API_KEY="..." # Windows PowerShell: $env:GEMINI_API_KEY="..."
```

3. Run the script:
```bash
python google-gemini-basic.py
```

## Output

When you run the script, it will send a basic user prompt to the model, which should provide a response:

```
User: How many tokens is your context window?
AI: I am a large language model, trained by Google. My context window is very large, but it is not a fixed number of tokens. It is more accurate to say that I can access information from a large amount of text provided in the prompt
```