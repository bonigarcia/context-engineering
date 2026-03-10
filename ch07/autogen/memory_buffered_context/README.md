# Buffered Memory with AutoGen

This example demonstrates how to manage short-term conversational memory using AutoGen's `BufferedChatCompletionContext`. This context manager keeps only a specified number of the most recent messages in the LLM's context window, preventing context overflow while maintaining conversational flow.

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
    python memory_buffered_context.py
    ```

## Expected Output

The `assistant` agent is configured with a `BufferedChatCompletionContext` with a buffer size of 3. After a few initial messages where the user states their name, and a few more messages are exchanged, a question is asked that relies on information outside this buffer. The expected output will show that the agent only remembers information within its configured memory window, demonstrating the effect of context buffering. The agent will likely *not* remember the user's name if it falls outside the buffer.

Example of a possible output:

```text
user_proxy (to assistant):

Hello!
--------------------------------------------------------------------------------
assistant (to user_proxy):

Hi there! How can I help you?
--------------------------------------------------------------------------------
user_proxy (to assistant):

My name is Alice.
--------------------------------------------------------------------------------
assistant (to user_proxy):

Nice to meet you, Alice!
--------------------------------------------------------------------------------
user_proxy (to assistant):

Tell me about the weather.
--------------------------------------------------------------------------------
assistant (to user_proxy):

I am not equipped to provide real-time weather information. TERMINATE
--------------------------------------------------------------------------------
user_proxy (to assistant):

What did I say was my name?
--------------------------------------------------------------------------------
assistant (to user_proxy):

I apologize, but I don't recall you mentioning your name earlier in this conversation. TERMINATE
--------------------------------------------------------------------------------
```