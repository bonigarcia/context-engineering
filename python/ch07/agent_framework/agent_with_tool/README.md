# Agent with Tool with Microsoft Agent Framework

This example demonstrates how to create an agent equipped with a custom tool using the Microsoft Agent Framework. The agent is designed to calculate the square of a number using a `calculate_square` function registered as a tool.


## Requirements

* [Python](https://www.python.org/) 3.10+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

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

3. Run the script:
```bash
python agent_with_tool.py
```

## Output

The agent will reply using the tool function defined: 

```
User: What's the weather in Madrid?
Agent response: It’s sunny in Madrid right now. Would you like the forecast or temperatures for today and the next few days?
```
