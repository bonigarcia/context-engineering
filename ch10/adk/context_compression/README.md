# Context compression Agent Development Kit (ADK)

This example demonstrates how to implement and use context compression within an ADK agent. It showcases how to manage and reduce the size of the conversation history passed to the LLM, improving efficiency and controlling token usage for longer interactions.

## Requirements

* [Python](https://www.python.org/) 3.10+
* A [Google API key](https://ai.google.dev/) set as an environment variable (`GOOGLE_API_KEY`)

## Steps for running this example in the shell

1. Install dependencies:
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
export GOOGLE_API_KEY="sk-..." # Windows cmd: set GOOGLE_API_KEY="sk-..." # Windows PowerShell: $env:GOOGLE_API_KEY="sk-..."
```

3. Run the script:
```bash
python context_compression.py
```

## Output

The agent will respond to user prompts, demonstrating efficient context handling. Example of a possible output:

```
[user]: Your long prompt here.
[root_agent]: The agent's concise response.
```
