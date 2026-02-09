# Human-in-the-Loop Evaluation with AutoGen

This example demonstrates how to implement Human-in-the-Loop (HITL) evaluation in AutoGen using the `UserProxyAgent`. By configuring the `UserProxyAgent` to always require human input (`human_input_mode="ALWAYS"`), you can ensure that a human operator reviews and provides feedback at each step of the agent's interaction. This approach is invaluable for evaluating agent behavior, steering conversations, and refining context in critical or complex tasks.

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
    Ensure your OpenAI API key is set as an environment variable.
    ```
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```

3.  Run the script:
    ```bash
    python human_in_the_loop_evaluation.py
    ```

## Expected Output

When you run this script, the `assistant` will propose a plan to write a Python script. After its first response, the `user_proxy_hitl` will prompt you for input in the console. This pause allows you, the human, to review the assistant's output, provide feedback, approve its plan, or steer it in a different direction. The conversation will only proceed after your input.

```text
user_proxy_hitl (to assistant):

Propose a plan to write a simple Python script that calculates the factorial of a number.
--------------------------------------------------------------------------------
assistant (to user_proxy_hitl):

Here's a plan to create a Python script to calculate the factorial of a number:

1.  **Define a function:** Create a Python function, for example, `calculate_factorial(n)`, that takes an integer `n` as input.
2.  **Base case:** Inside the function, handle the base case: if `n` is 0 or 1, the factorial is 1.
3.  **Recursive/Iterative step:** For `n > 1`, calculate the factorial either recursively (`n * calculate_factorial(n-1)`) or iteratively using a loop.
4.  **Main execution block:**
    *   Prompt the user to enter a number.
    *   Convert the input to an integer.
    *   Call the `calculate_factorial` function with the user's input.
    *   Print the result.
5.  **Error handling (optional but recommended):** Add a `try-except` block to handle cases where the user inputs non-integer values or negative numbers.

Once you approve this plan, I can start writing the code.
--------------------------------------------------------------------------------
Provide feedback to assistant. Press enter to skip and use auto-reply, or type 'exit' to terminate the conversation:
```
At this point, you can type your feedback or simply press Enter to let the agent continue. Type `exit` to terminate the conversation. This continuous human intervention highlights the HITL aspect of the evaluation.