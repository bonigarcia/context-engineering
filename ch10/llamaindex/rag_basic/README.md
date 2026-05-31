# Basic RAG example with LlamaIndex

This example demonstrates a basic Retrieval-Augmented Generation (RAG) setup using LlamaIndex. It loads text from a local file, creates a vector store index, and then queries the index to retrieve relevant information.

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
python rag_basic.py
```

## Output

The script will print the answer to the query "What is LlamaIndex?" based on the content of the `data.txt` file.
