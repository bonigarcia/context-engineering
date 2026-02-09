# ADK memory example

This example demonstrates how to use the ADK's `InMemoryMemoryService` to manage long-term conversational memory across different sessions. It shows how an agent can capture information in one session and another agent can recall it in a subsequent session using a memory retrieval tool.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your Google API key (`GOOGLE_API_KEY`) is set as an environment variable.

3. Run the script:
```bash
python memory_example.py
```

## Expected Output

The script will execute two distinct scenarios:

* Turn 1: An `InfoCaptureAgent` will acknowledge a user's statement, and the session's content will be added to the `InMemoryMemoryService`.
* Turn 2: A `MemoryRecallAgent` (equipped with a `load_memory` tool) will be queried. It should recall the information captured in Turn 1 from the memory service.
