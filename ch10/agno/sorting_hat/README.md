# Sorting Hat

This example uses Agno's real `Agent` and `Workspace` APIs to inspect the local `ch10/agno` directory.

The important part is the boundary: the agent only gets read-style workspace access, so it can inventory the folder without seeing the rest of the repository. That makes it a good fit for Agno's runtime/control-plane model, where the same agent can later be managed, traced, and served through AgentOS.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [OpenAI API key](https://platform.openai.com/api-keys) set as an environment variable (`OPENAI_API_KEY`)

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
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python sorting_hat.py
```

## What it demonstrates

- Scoped workspace access to local files.
- A single agent that reasons over its own project folder.
- A clear path from ad-hoc script to managed AgentOS service.

## Output

When you run the script, it will print the results to the terminal.
