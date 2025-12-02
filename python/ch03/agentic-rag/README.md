# Agentic retrieval-augmented generation (RAG)

This sample application implements an agentic RAG system using the following stack:

- LLM: [Llama 3.2 1B](https://ollama.com/library/llama3.2:1b) via [Ollama](https://ollama.com/download)
- Agent framework: [LangChain](https://www.langchain.com/)
- Embedding model: [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- Vector database: [FAISS](https://faiss.ai/) (in-memory)

This example demonstrates how an agent can decide whether to use a RAG tool to answer a question.

### Requirements

To run this example, you need the following:

- [Python](https://www.python.org/)
- [Ollama](https://ollama.com/)

### Steps for running this example

1. Pull Llama 3.2 1B with Ollama:
```bash
ollama pull llama3.2:1b
```

2. Get the Python sources and go to the example directory:
```bash
git clone https://github.com/bonigarcia/context-engineering
cd context-engineering/python/ch03/agentic-rag
```

3. Create a virtual environment and activate it (optional, but recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

5.  Run the Agentic RAG example script:
```bash
python3 agentic_rag.py
```

### Output

After running the script, you will see the agent answering questions. For the first question, it will use its internal knowledge. For the second question, it will use the RAG tool to find the answer in the provided documents.

```
> Entering new AgentExecutor chain...
I am not aware of a person named "Boni Garcia". I can provide information on well-known individuals if you can clarify the name.

> Finished chain.

> Entering new AgentExecutor chain...
Invoking: `search_documents` with `{'query': 'Who is the author of the book "Context Engineering for Generative AI"?'}`
Tool result: The author of the book "Context Engineering for Generative AI" is Boni Garcia.
The author of the book "Context Engineering for Generative AI" is Boni Garcia.

> Finished chain.
```
