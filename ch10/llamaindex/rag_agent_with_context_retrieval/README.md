# RAG Agent with Context Retrieval in LlamaIndex

This example demonstrates how to create a LlamaIndex agent that performs retrieval-augmented generation (RAG) by fetching relevant context *before* deciding to call a tool or directly answer a query. This approach ensures that the agent's decisions and responses are grounded in external knowledge.

The example sets up a simple RAG system with a `VectorStoreIndex` from a dummy document. It then defines a custom tool and integrates it with an `OpenAIAgent`, augmenting the agent with a context retriever. The agent will use the retrieved context to make more informed decisions when responding to user queries, potentially using the tool only when necessary.

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
python rag_agent_with_context_retrieval.py
```

## Output

The script will demonstrate an interaction with the agent. It will answer a question using its base knowledge first, then it will process a query that requires retrieving information from the provided context, and finally, it will use the tool if the question is relevant to it.
