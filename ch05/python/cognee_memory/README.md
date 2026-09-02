# Basic memory with Cognee

This example demonstrates how to set up [Cognee](https://cognee.ai/) to build a persistent memory layer using a knowledge engine approach (Vector search + Knowledge Graph).

## A note on the Cognee API

This example uses `add()`, `cognify()`, `search()`, and the `prune` helpers, which is the API surface described in Chapter 5. Recent Cognee releases also expose a higher-level surface built around `remember()`, `recall()`, `forget()`, and `improve()`, which wraps the same ingestion and retrieval pipeline behind fewer calls. Both work with the pinned dependency. The lower-level calls are kept here because they make each stage of the memory pipeline visible, which is the point of the example.

## Requirements

* [Python](https://www.python.org/) 3.10+
* A model API key exposed as `LLM_API_KEY` (for example, an [OpenAI API key](https://platform.openai.com/api-keys))

## Steps for running this example in the shell

1.  Install dependencies:
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

2. Export your model API key as an environment variable:
```bash
export LLM_API_KEY="sk-..." # Windows cmd: set LLM_API_KEY="sk-..." # Windows PowerShell: $env:LLM_API_KEY="sk-..."
```

3. Run the script:
```bash
python cognee_memory.py
```

## Output

When you run the script, it will add a short text piece to the Cognee memory layer, "cognify" it (processing it into a knowledge graph and vectorizing it), and then perform a hybrid search to retrieve it.

```text
=== Cognee Memory Example ===
Pruning old data...
Storage manager absolute path: ...\.venv\Lib\site-packages\cognee\.cognee_cache
Deleting cache...
✓ Cache deleted successfully!
Adding context to memory...
User 48a79c34-ee78-4f81-afcc-81947dc8a4df has registered.
Data added: 'Context engineering is the process of optimizing information provided to an LLM to improve its performance and accuracy.'
Cognifying (building knowledge graph and vector index)...
Searching memory for: 'What is context engineering?'
--- Memory Retrieval Results ---
Result 1: {'dataset_id': UUID('db5e4b38-8ece-5953-bbf1-dd723eee7283'), 'dataset_name': 'main_dataset', 'dataset_tenant_id': None, 'search_result': ['Context engineering is the process of optimizing the information supplied to a large language model (LLM) to improve its effectiveness, accuracy, and overall performance.']}
```
