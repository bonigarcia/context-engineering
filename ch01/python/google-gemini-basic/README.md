# Basic interaction with Google Gemini models

This example demonstrates how to set up a [Google Gemini](https://gemini.google.com/) model and send a basic user prompt with Python.

## Requirements

* [Python](https://www.python.org/) 3.6+
* A [Google API key](https://aistudio.google.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Export your Google API key as an environment variable:
```bash
export GOOGLE_API_KEY="..." # Windows cmd: set GOOGLE_API_KEY="..." # Windows PowerShell: $env:GOOGLE_API_KEY="..."
```

3. Run the script:
```bash
python google-gemini-basic.py
```

## Output

When you run the script, it will send a user prompt to a Gemini model (`gemini-2.5-flash`). Then, it will send the same user prompt to a more advanced model (`gemini-3.1-flash-lite-preview`). The output will show the responses from both models.

```
=== Basic model  ===
User: How many tokens is your context window?
        Latency: 2.679 seconds
        Prompt tokens: 9
        Cached prompt tokens: None
        Output tokens: 96
        Thinking tokens: 395
        Total tokens: 500
Gemini-2.5: As a large language model, I don't have a "context window" in the traditional sense that a human or a specific software application might. My architecture and the specific parameters, including the maximum amount of information I can process in a single turn or maintain across a conversation, are technical details set by my developers (Google).

This information is proprietary and not something I can disclose. However, I am designed to handle substantial amounts of text and maintain context over lengthy conversations.

=== Advanced model  ===
User: How many tokens is your context window?
        Latency: 1.430 seconds
        Prompt tokens: 9
        Cached prompt tokens: None
        Output tokens: 93
        Thinking tokens: 142
        Total tokens: 244
Gemini-3.1: I am a large language model, trained by Google.

My context window size depends on the specific version of the model you are interacting with. Currently, many versions of Gemini (such as Gemini 1.5 Pro) support a context window of **up to 2 million tokens**.

This allows me to process and "remember" a vast amount of information in a single conversation, including long documents, large codebases, or hours of video and audio.
```