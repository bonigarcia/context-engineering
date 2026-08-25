# Streaming responses from Google Gemini models

This example demonstrates how to stream the response of a [Google Gemini](https://gemini.google.com/) model with Python. Instead of waiting for the complete answer, the script prints each fragment as the model produces it and reports the time to first token.

## Requirements

* [Python](https://www.python.org/) 3.8+
* A [Google API key](https://aistudio.google.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Export your API key as an environment variable:
```bash
export GOOGLE_API_KEY="..." # Windows cmd: set GOOGLE_API_KEY="..." # Windows PowerShell: $env:GOOGLE_API_KEY="..."
```

3. Run the script:
```bash
python google-gemini-streaming.py
```

## Output

When you run the script, it sends a user prompt to a Gemini model (`gemini-2.5-flash`) and prints the answer as it is generated. Once the stream ends, it prints the time to first token, the total latency, and the token counts. Each streamed chunk can carry usage metadata, so the script keeps the last one it sees and reports it after the stream ends.
