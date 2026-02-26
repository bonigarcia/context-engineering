# Policy enforcement: regulating AI tool usage

This example demonstrates a "policy as code" approach to govern how AI agents use external tools. It simulates an enforcement point that validates tool arguments against a set of security rules.

## Requirements

This project requires [Python](https://www.python.org/) 3.x. No external libraries are required (the script uses standard Python logic).

## Steps for running this example

1. Run the script:
```bash
python policy_enforcement.py
```

## Output

The script will attempt to execute two tool calls (one safe, one restricted) and show how the policy engine intercepts the unauthorized action.

```text
[INFO] User 'marketing_intern' attempting to call 'list_files'...
[SUCCESS] Policy evaluation: ALLOW.
[INFO] User 'marketing_intern' attempting to call 'delete_database'...
[FAILURE] Policy evaluation: DENY. Reason: User lacks 'admin' role required for 'delete_database'.
```