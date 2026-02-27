# PII redaction with Microsoft Presidio

This example demonstrates how to use the [Microsoft Presidio](https://microsoft.github.io/presidio/) framework to identify and redact sensitive information from text. The provided script leverages natural language processing to detect various types of personally identifiable information. This includes entities such as names and email addresses as well as phone numbers and locations. Once detected, the system applies a redaction policy to replace these sensitive values with a standard placeholder.

## Requirements

This project requires [Python](https://www.python.org/) 3.9+, the libraries listed in `requirements.txt`, and a [spaCy](https://spacy.io/) model (`en_core_web_lg`).

## Steps for running this example

1. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Download the required NLP model:
```bash
python -m spacy download en_core_web_lg
```

3. Run the Presidio script:
```bash
python presidio_example.py
```

Output
======
The script will identify sensitive entities and replace them with placeholders.

```text
Analyzing text for PII...
Anonymizing sensitive entities...
--------------------
Original Text: Hello, my name is David Miller. You can reach me at david.miller@example.com or by phone at 212-555-0123. I live at 123 Main St, New York.
--------------------
Anonymized Text: Hello, my name is <REDACTED>. You can reach me at <REDACTED> or by phone at <REDACTED>. I live at 123 <REDACTED>, <REDACTED>.
```