# Pipeline composition

This example composes a small Haystack pipeline out of separate retrieval, context assembly, and response formatting stages.

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
python haystack_pipeline_composition.py
```

## Output

```
Question: organize notes
Pipeline composition answer:
- retrieval gathers the local notes
- assembly turns them into a readable context
- final context:
Pipeline composition: Haystack pipelines keep retrieval, assembly, and formatting separate when you organize notes.
Single-purpose stages: A small pipeline is easier to test when each component does one job.
```
