# Context compression with LangChain

This example demonstrates how to compress retrieved context before it reaches an LLM. A base retriever fetches candidate documents, and an extractor chain built with LangChain Expression Language keeps only the passages that are relevant to the query. This technique helps reduce token usage and improve the relevance of responses by eliminating noise from retrieved contexts.

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
python context_compression.py
```

## Output

When you run the script, it will first show documents retrieved by a standard retriever. Then, it will demonstrate how the compression chain processes these documents, extracting only the most relevant sentences or phrases pertaining to the query. Finally, it will conceptually show an LLM generating a response using this compressed context.

Example output:

```
Query: What is contextual compression in LangChain?

--- Retrieved documents (without compression) ---
Document 1 (Source: doc3):
Contextual compression reduces the noise in retrieved documents. This helps LLMs focus on relevant information. It's especially useful when the retrieved chunks contain a lot of irrelevant detail around the answer.
---
Document 2 (Source: doc4):
LangChain provides tools like LLMChainExtractor for post-processing retrieved documents to make them more concise and relevant to the query.
---

--- Retrieved documents (with contextual compression) ---
Document 1 (Source: doc3):
Contextual compression reduces the noise in retrieved documents. This helps LLMs focus on relevant information.
---
Document 2 (Source: doc4):
LangChain provides tools like LLMChainExtractor for post-processing retrieved documents to make them more concise and relevant to the query.
---

--- LLM response using compressed context (conceptual) ---
Contextual compression in LangChain refers to the process of reducing noise and extracting only the most relevant information from retrieved documents before passing them to a Large Language Model (LLM). This technique, often implemented using tools like LLMChainExtractor, helps LLMs focus on pertinent data, leading to more concise and accurate responses.
```
