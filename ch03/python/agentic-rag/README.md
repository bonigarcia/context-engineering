# Agentic retrieval-augmented generation (RAG)

This sample application implements an agentic RAG system using the following stack:

* LLM: [Llama 3.1 8B](https://ollama.com/library/llama3.1) via [Ollama](https://ollama.com/download)
* Agent framework: [LangChain](https://www.langchain.com/)
* Embedding model: [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
* Vector store: `InMemoryVectorStore` (included in `langchain-core`)

This example demonstrates how an agent can decide whether to use a RAG tool to answer a question.

## Requirements

* [Python](https://www.python.org/) 3.6+
* [Ollama](https://ollama.com/)

## Steps for running this example in the shell

1. Pull Llama 3.1 8B with Ollama:
```bash
ollama pull llama3.1:8b
```

The model has to support tool calling, because the agent decides whether to retrieve by emitting a tool call. It also needs enough capacity to answer from the retrieved passages. Smaller models such as `llama3.2:3b` emit the tool call correctly but often ignore the retrieved text and reply that they found no information.

2. Install dependencies:
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

3. Run the script:
```bash
python agentic_rag.py
```

### Output

After running the script, you will see the agent answering a question. It will use the RAG tool to find the answer in the provided documents.

```
Who is the author of the book 'Fake Book: The New Age'?

The author of the book 'Fake Book: The New Age' is George Cauldron.
```