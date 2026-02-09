# Google search example

This example demonstrates how to integrate Google Search as a grounding tool within an ADK agent, allowing the agent to retrieve real-time information from the web to answer user queries.

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
python google_search.py
```

## Expected Output

The agent will respond to your queries, potentially using Google Search to find the answer. You will observe the agent's thought process, including when it decides to invoke the search tool and the results it obtains.