# Basic memory with Cognee

This example demonstrates how to set up [Cognee](https://cognee.ai/) to build a persistent memory layer using a knowledge engine approach (Vector search + Knowledge Graph).

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [OpenAI API key](https://platform.openai.com/api-keys) (used by default by Cognee)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Export your OpenAI API key as an environment variable:
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
