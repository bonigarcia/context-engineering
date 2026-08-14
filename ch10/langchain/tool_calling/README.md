# Tool calling with LangChain agents

This example demonstrates how to empower a LangChain agent with custom tools, enabling the LLM to perform actions beyond its internal knowledge. It showcases the creation of a simple tool and an agent configured to use it, illustrating how the LLM decides when and how to invoke the tool to answer specific queries.

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
python tool_calling.py
```

## Output

When you run the script, the model receives a query that cannot be answered
without the policy tool. The model issues a tool call, the script executes the
tool and appends its result to the message list, and the model is invoked again
to produce the final answer. Only that final answer is printed.

Example output:

```
No — refunds over €100 require human approval.

What to do next
- Escalate the request to the authorized approver (manager/finance team/approval queue).
- Include these details in the escalation:
  - Customer name and contact
  - Order number / transaction ID
  - Refund amount: €250
  - Reason for refund and any relevant notes
  - Original payment method and date
  - Supporting evidence (receipts, screenshots, correspondence)
  - Desired outcome (full refund, partial, store credit)
  - Any policy exceptions requested

Quick approval-request template you can copy/paste
"Please approve a €250 refund for Order #[ORDER_ID] (Customer: [NAME]). Reason: [SHORT REASON]. Supporting docs attached: [list]. Original payment: [METHOD, DATE]. Requested by: [YOUR NAME]."

If you tell me which approval channel you use (email, ticket system, Slack, etc.) or give the order details, I can draft the exact message/ticket for you.
```
