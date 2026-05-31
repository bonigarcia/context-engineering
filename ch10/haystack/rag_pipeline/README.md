# RAG pipeline

This example uses a local Haystack pipeline with an in-memory document store and BM25 retrieval.

## Requirements

* [Python](https://www.python.org/) 3.10+

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

2. Run the script:
```bash
python haystack_rag_pipeline.py
```

## Output

```
Question: How do I keep notes organized?
Retrieved context:
- Organizing with tags: Use tags to group related notes and keep the workspace tidy.
- Archiving old notes: Archive finished notes instead of deleting them so they stay searchable.
```
