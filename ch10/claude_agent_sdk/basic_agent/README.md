# Basic agent with the Claude Agent SDK

This example runs the agent loop behind Claude Code as a library, using the [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview). The options set the harness defaults before the loop starts: the system prompt, the tools the agent may use, the permission mode that governs approvals, and the maximum number of turns.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [Anthropic API key](https://console.anthropic.com/) set as an environment variable (`ANTHROPIC_API_KEY`)
* The Claude Code CLI available on the `PATH`, since the SDK runs it as a subprocess (`npm install -g @anthropic-ai/claude-code`)

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
export ANTHROPIC_API_KEY="sk-ant-..." # Windows cmd: set ANTHROPIC_API_KEY="sk-ant-..." # Windows PowerShell: $env:ANTHROPIC_API_KEY="sk-ant-..."
```

3. Run the script:
```bash
python basic_agent.py
```

## Output

When you run the script, the agent reads the files it is allowed to read and streams the messages of the loop to the terminal, ending with its summary.
