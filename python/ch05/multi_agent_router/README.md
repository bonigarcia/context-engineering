# Multi-Agent Router Pattern

This example demonstrates the **router multi-agent pattern** using `langgraph`. It simulates a customer support system that intelligently routes user questions to specialized agents (Sales, Technical Support, or General) based on the query's intent.

## Setup

1.  **Install dependencies**:
    Navigate to the `python/ch05/multi_agent_router` directory and install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set environment variables**:
    Ensure your OpenAI API key is set as an environment variable. You can do this by:
    ```bash
    export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```
    Alternatively, create a `.env` file in the `multi_agent_router` directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

## Run the example

Execute the Python script:

```bash
python multi_agent_router.py
```

The script will run three example questions, demonstrating how the system routes each query to the appropriate specialized agent and generates a response.
