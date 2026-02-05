# Multi-Agent conversation with AutoGen

This example demonstrates a basic multi-agent conversation using AutoGen, where an `AssistantAgent` and a `UserProxyAgent` collaborate to solve a task. The `AssistantAgent` is configured to be a helpful AI assistant that can write and execute Python code. The `UserProxyAgent` acts as a proxy for the human user, allowing the assistant to generate code and receive feedback (in this case, code execution results).

## Requirements

* [Python](https://www.python.org/) 3.8+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

3. Run the script:
```bash
python multi_agent_conversation.py
```


## Expected Output

The agents will engage in a conversation to determine the 10th Fibonacci number. The `AssistantAgent` will likely write Python code to calculate it, and the `UserProxyAgent` will execute the code. The output will show the conversational flow and the final result.

Example of a possible output:

```
user_proxy (to assistant):

What is the 10th Fibonacci number? Write and execute Python code to find it.

--------------------------------------------------------------------------------
assistant (to user_proxy):

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a

print(fibonacci(10))
```

--------------------------------------------------------------------------------
user_proxy (to assistant):

exitcode: 0
arguments:
(1) print(fibonacci(10))
9
9

--------------------------------------------------------------------------------
assistant (to user_proxy):

The 10th Fibonacci number is 34.
TERMINATE

--------------------------------------------------------------------------------
```