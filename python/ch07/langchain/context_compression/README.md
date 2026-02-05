# Context compression with LangChain

This example demonstrates how to use LangChain's `ContextualCompressionRetriever` to optimize the context provided to an LLM. It shows how a base retriever can fetch relevant documents, and then an `LLMChainExtractor` (powered by an LLM) can further process and compress these documents, extracting only the most pertinent information before it's passed to the final LLM prompt. This technique helps reduce token usage and improve the relevance of responses by eliminating noise from retrieved contexts.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```
Alternatively, create a `.env` file in the source directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

3. Run the script:
```bash
python context_compression.py
```


## Output

When you run the script, it will first show documents retrieved by a standard retriever. Then, it will demonstrate how the `ContextualCompressionRetriever` processes these documents, extracting only the most relevant sentences or phrases pertaining to the query. Finally, it will conceptually show an LLM generating a response using this compressed context.

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
