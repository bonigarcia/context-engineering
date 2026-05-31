# Agent with memory using Microsoft Agent Framework

This example demonstrates how to add memory to a Microsoft Agent Framework agent using a custom `ContextProvider`, i.e., a `UserInfoMemory` as follows:

- `invoked`: runs after each agent call and extracts name/age from user messages.
- `invoking`: runs before each agent call and injects memory into the prompt as instructions.
- `serialize`: returns JSON so memory can be persisted with the thread/session.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [OpenAI API key](https://platform.openai.com/api-keys) set as an environment variable (`OPENAI_API_KEY`)

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

2. Export your API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python agent_with_memory.py
```

## Output

The script will demonstrate the agent's ability to remember user facts:

```
Agent ready. Type 'exit' to quit.

Try asking a question first — it should request name/age.

You: What is 2+2?

Agent: I’d be happy to help with that, but first, could you please tell me your name?

You: John

Agent: Nice to meet you, John! Can you also tell me your age?

You: 25

Agent: Thank you for sharing that, John! Now, to answer your question, 2 + 2 equals 4. If you have any more questions, feel free to ask!
```
