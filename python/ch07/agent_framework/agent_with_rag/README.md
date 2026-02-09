# Agent with RAG using Microsoft Agent Framework

This example demonstrates how to augment an AI agent with Retrieval Augmented Generation (RAG) capabilities using the Microsoft Agent Framework's `AIContextProvider`. The agent will use provided external context to answer questions, ensuring responses are grounded in the given information.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Setup

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
   Ensure your API keys are set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
AZURE_AI_SEARCH_ENDPOINT="YOUR_AZURE_AI_SEARCH_ENDPOINT"
AZURE_AI_SEARCH_API_KEY="YOUR_AZURE_AI_SEARCH_API_KEY"
```

3. Run the script:
```bash
python agent_with_rag.py
```

## Output

The script will demonstrate the agent's ability to answer questions based on the content of some external knowledge. You should observe responses that are specifically grounded in the provided context.