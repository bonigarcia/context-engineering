# ADK memory example

This example demonstrates how to use the ADK's `InMemoryMemoryService` to manage long-term conversational memory across different sessions. It shows how an agent can capture information in one session and another agent can recall it in a subsequent session using a memory retrieval tool.

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
python memory_example.py
```

## Output

The script will execute two distinct scenarios:

* Turn 1: An `InfoCaptureAgent` will acknowledge a user's statement, and the session's content will be added to the `InMemoryMemoryService`.
* Turn 2: A `MemoryRecallAgent` (equipped with a `load_memory` tool) will be queried. It should recall the information captured in Turn 1 from the memory service.
