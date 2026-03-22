# Context-augmented generation (user-level context)

This example demonstrates a context-augmented generation pattern using a LLM. Instead of performing a retrieval step for every user query, we identify the relevant domain information up front and inject it directly into the user prompt.

In this example, the context is injected into the user prompt.

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
python context-augmented-generation-user-prompt.py
```

## Output

When you run the script, it will send a single text prompt to a GPT model (`gpt-4o-mini`). This prompt includes a reference manual for an espresso machine and the user's question. The model will use this manual to answer the question about error code E17, citing the relevant sections.

```
User: The machine shows error code E17 after I finished descaling. What should I do?

Response:
Error code E17 indicates that the descale cycle is incomplete, which means the machine detected residual descaling solution or scale (see Section 4: Error codes). 

To resolve this issue, please follow these steps from Section 5: "Resolving error code E17":

1. **Verify Rinse Cycles**: Confirm that you have completed the full descaling procedure as described in Section 2, including running two full tanks of fresh water through the system after descaling (the rinse cycles).
2. **Check Reservoir**: Ensure that the water reservoir is filled only with fresh water and that no descaling solution remains.
3. **Run Additional Rinse**: Execute one more rinse cycle using fresh water.
4. **Restart the Machine**: If the error persists, unplug the machine for 5 minutes and then restart it.
5. **Contact Support**: If E17 still appears after following these steps, contact customer support with your machine’s serial number for further assistance.

By following these procedures, you ensure that the machine is properly cleared of any residual minerals or solution.
```
