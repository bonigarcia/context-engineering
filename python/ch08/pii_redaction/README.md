# PII redaction: privacy guardrails

This example demonstrates how to implement a basic privacy guardrail that redacts _personally identifiable information_ (PII) before it is sent to an external LLM.

## Requirements

This project requires [Python](https://www.python.org/) 3.x. No external libraries are required (the script uses standard Python logic).

## Steps for running this example

1. Run the script:
   ```bash
   python pii_redaction.py
   ```

## Output

The script will process a sample message and display the redacted version.

```text
[INFO] Original Message:
Hello, my name is John Doe. My email is john.doe@example.com and my phone number is 555-123-4567. I live at 123 Maple St.

[INFO] Redacting PII...
[INFO] Redacted Message:
Hello, my name is [NAME]. My email is [EMAIL] and my phone number is [PHONE]. I live at [ADDRESS].
```