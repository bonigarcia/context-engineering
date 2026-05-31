# Agent with custom tool in LlamaIndex

This example demonstrates how to create a LlamaIndex agent capable of using custom tools to extend its capabilities beyond its core knowledge. Tools allow agents to interact with the external environment, perform specific actions, or retrieve information that is not available in their pre-trained data or through RAG.

In this example, a simple `get_current_weather` tool is defined and then provided to a LlamaIndex `FunctionAgent`. The agent can then decide when to use this tool based on the user's query.

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
python agent_with_tool.py
```

## Output

The script will demonstrate an interaction with the agent. The agent will respond to queries about the weather by utilizing the `get_current_weather` tool when appropriate.
