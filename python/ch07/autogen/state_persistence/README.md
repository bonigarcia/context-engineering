# Agent State Persistence in AutoGen

This example demonstrates how to save and load the state of an AutoGen `AssistantAgent`. This feature is crucial for maintaining conversational continuity across sessions, enabling agents to remember user preferences or past interactions even after their instances are re-initialized.

## Requirements

*   [Python](https://www.python.org/) 3.8+
*   An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Steps for running this example

1.  Install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2.  Set environment variables:
    Ensure your OpenAI API key is set as an environment variable. You can do this by:
    ```
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```

3.  Run the script:
    ```bash
    python state_persistence.py
    ```

## Expected Output

The script will first initiate a conversation where the user tells the assistant their favorite color. After this interaction, the assistant's state is saved. A new assistant instance is then created and its state is loaded from the saved data. When asked about the favorite color again, the restored assistant will correctly recall the information, demonstrating successful state persistence.

Example of a possible output:

```text
--- First Interaction: Establishing a preference ---
user_proxy (to assistant):

My favorite color is blue. Can you remember that?
--------------------------------------------------------------------------------
assistant (to user_proxy):

Okay, I'll remember that your favorite color is blue. TERMINATE

--- Saved state of assistant ---
{
  "llm_context": {
    "messages": [
      {
        "content": "You are a helpful AI assistant. Remember user preferences. Respond with 'TERMINATE' when the task is done.",
        "type": "SystemMessage"
      },
      {
        "content": "My favorite color is blue. Can you remember that?",
        "source": "user_proxy",
        "type": "UserMessage"
      },
      {
        "content": "Okay, I'll remember that your favorite color is blue. TERMINATE",
        "name": "assistant",
        "type": "AssistantMessage"
      }
    ]
  },
  "type": "AssistantAgentState"
}

--- Second Interaction: Resuming conversation with restored state ---
user_proxy (to assistant):

What is my favorite color?
--------------------------------------------------------------------------------
assistant (to user_proxy):

Your favorite color is blue. TERMINATE
--------------------------------------------------------------------------------
```
The exact content of the "Saved state" JSON may vary slightly but will contain the conversation history reflecting the learned preference.