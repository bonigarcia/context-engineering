# Tool calling with LangChain agents

This example demonstrates how to empower a LangChain agent with custom tools, enabling the LLM to perform actions beyond its internal knowledge. It showcases the creation of a simple tool and an agent configured to use it, illustrating how the LLM decides when and how to invoke the tool to answer specific queries.

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
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```
Alternatively, create a `.env` file in the source directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

3. Run the script:
```bash
python tool_calling.py
```

## Output

When you run the script, it will execute an agent that processes several queries. For queries requiring external information (like the current time or date), the agent will utilize the `get_current_time` tool. The output will show the agent's thought process (due to `verbose=True`) and its final responses.

Example output:

```
--- Query 1: Get current time ---
> Entering new AgentExecutor chain...
... (agent's thought process using the tool) ...
Agent response: The current time is HH:MM:SS (actual time will vary).

--- Query 2: Get current date in a specific format ---
> Entering new AgentExecutor chain...
... (agent's thought process using the tool) ...
Agent response: Today's date is YYYY-MM-DD (actual date will vary).

--- Query 3: A simple question not requiring tools ---
> Entering new AgentExecutor chain...
... (agent's thought process, not calling the tool) ...
Agent response: The capital of Spain is Madrid.
```
