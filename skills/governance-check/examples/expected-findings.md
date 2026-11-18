# Expected findings for examples/agent-config

A correct review reports at least these high-severity problems:

- Indirect prompt injection: `read_url` brings any web page into the context, and the system prompt tells the agent to take its content into account. A page can carry instructions.
- Exfiltration: `send_email` accepts any recipient, so injected instructions (or a manipulated customer conversation) can send data anywhere. Restrict the recipient to the customer's verified address.
- No human oversight on money: `issue_refund` takes effect immediately with no approval step or amount limit, based on the model's judgment that a reason "seems valid".
- Personal data in logs: full conversations with personal data are kept for 5 years and readable by three teams. Redact, shorten retention, and restrict access.

The review should note that the combination of untrusted reading (`read_url`) and side-effect tools (`send_email`, `issue_refund`) in one agent is the core risk.
