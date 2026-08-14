# Retrieval-Augmented Generation (RAG) with LangChain

This example demonstrates how to implement a basic Retrieval-Augmented Generation (RAG) system using LangChain. It showcases loading a document, splitting it into chunks, generating embeddings, storing them in an in-memory vector store, and then retrieving relevant information to answer a query using an LLM. The vector store is `InMemoryVectorStore`, which ships with `langchain-core` and needs no extra dependency.

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
python rag_with_vectorstore.py
```

## Output

When you run the script, it will perform the following actions:
1.  Create a temporary `sample_document.txt` with some dummy text.
2.  Load and split this document.
3.  Create embeddings and store them in an `InMemoryVectorStore`.
4.  Retrieve relevant chunks for the question "What is RAG and why is it useful?".
5.  Use an LLM to answer the question based on the retrieved context.
6.  Print the query, the LLM's answer, and the metadata of the source documents used.
7.  Clean up the temporary `sample_document.txt`.

The output should look similar to this:

```
Query: What is RAG and why is it useful?
Response: RAG (Retrieval-Augmented Generation) is an approach that combines large language models with external knowledge bases. It is useful because it lets the LLM retrieve relevant information from those external sources and use it to produce more accurate and up-to-date responses. Tooling like LangChain (document loaders, text splitters, embedding models, vector stores, retrievers) and libraries such as FAISS (for efficient similarity search of dense vectors) support building RAG systems.
Source Documents: [{'source': 'sample_document.txt'}]
```
(Note: The metadata for the source documents will be empty as they are generated on the fly for this example.)
