# Query expansion

This example expands a user query into a few local variants, runs BM25 retrieval for each variant, and merges the results.

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
python haystack_query_expansion.py
```

## Output

```
Question: sync notes
Expanded retrieval:
- Syncing notes: Sync notes from every device after you sign in.
- Organizing notes: Organize notes with tags and folders.
- Backing up notes: Backup notes regularly so you can restore them later.
```
