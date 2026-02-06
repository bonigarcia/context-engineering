# Agent with tool in AutoGen

This example demonstrates how to define and use a custom tool with an AutoGen agent. The `AssistantAgent` is given access to a `calculate_square` function, which it can use to answer questions requiring this specific calculation. The `UserProxyAgent` registers this tool and makes it available to the assistant.

## Requirements

* [Python](https://www.python.org/) 3.8+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
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

## Expected Output

The agents will engage in a conversation where the `AssistantAgent` will identify the need to use the `calculate_square` tool to answer the question. The `UserProxyAgent` will facilitate the tool execution.

Example of a possible output:

```
user_proxy (to assistant):

What is the square of 15? Use the calculate_square tool.

--------------------------------------------------------------------------------
assistant (to user_proxy):

I need to calculate the square of 15. I will use the `calculate_square` tool.
print(calculate_square(15))

--------------------------------------------------------------------------------
user_proxy (to assistant):

exitcode: 0
arguments:
(1) calculate_square(15)
225

--------------------------------------------------------------------------------
assistant (to user_proxy):

The square of 15 is 225.
TERMINATE

--------------------------------------------------------------------------------
```