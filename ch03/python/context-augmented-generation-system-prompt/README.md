# Context-augmented generation (system-level context)

This example demonstrates a context-augmented generation pattern using a LLM. Instead of performing a retrieval step for every user query, we identify the relevant domain information up front and inject it directly into the user prompt.

In this example, the context is injected into the system prompt.

## Requirements

* [Python](https://www.python.org/) 3.6+
* An [OpenAI API key](https://platform.openai.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python context-augmented-generation-system-prompt.py
```

## Output

When you run the script, it will send a user prompt to a GPT model (`gpt-4o-mini`) using a system prompt that includes a reference manual for an espresso machine. The model will use this manual to answer the user's question about error code E17.

```
User: The machine shows error code E17 after I finished descaling. What should I do?

Response:
Error code E17 indicates that the descale cycle is incomplete, which means the machine detected residual descaling solution or scale. To resolve this, please follow these steps from Section 5, "Resolving error code E17":

1. **Verify Descaling Procedure**: Confirm that you have completed the full descaling procedure as outlined in Section 2, including both of the required rinse cycles.
2. **Inspect Water Reservoir**: Check the water reservoir to ensure it is filled only with fresh water and that there is no descaling solution remaining.
3. **Run Additional Rinse**: Perform one more rinse cycle using fresh water to clear out any remaining deposits.
4. **Restart the Machine**: If the error persists after rinsing, unplug the machine from its power source for 5 minutes, then plug it back in and restart it.
5. **Contact Support**: If E17 still appears after these steps, please contact customer support and provide your machine’s serial number for further assistance.
```