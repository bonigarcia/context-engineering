# Context compression Agent Development Kit (ADK)

This example demonstrates how to implement and use context compression within an ADK agent. It showcases how to manage and reduce the size of the conversation history passed to the LLM, improving efficiency and controlling token usage for longer interactions.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

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

2. Set environment variables:
   Ensure your Google API key (`GOOGLE_API_KEY`) is set as an environment variable.

3. Run the script:
```bash
python context_compression.py
```

## Expected Output

The agent will respond to user prompts, demonstrating efficient context handling. Example of a possible output:

```
[user]: Your long prompt here.
[root_agent]: The agent's concise response.
```
