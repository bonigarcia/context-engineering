# Memory Handoff

This example shows CrewAI memory in action: one task records notes and the next task reuses them as context.

## Prerequisites

- Python 3.13+
- OpenAI API Key (configured via `OPENAI_API_KEY` environment variable)

## Steps for running this example

1.  Install dependencies:
```bash
py -3.13 -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Set environment variables:
   Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

3. Run the script:
```bash
python memory_handoff.py
```

## Output

The script will print the initial notes and the final output to the console.

```
╭───────────────────────────────────────────────────────────────── ✅ Agent Final Answer ──────────────────────────────────────────────────────────────────╮
│                                                                                                                                                          │
│  Agent: Responder                                                                                                                                        │
│                                                                                                                                                          │
│  Final Answer:                                                                                                                                           │
│  Effective memory handoff is the process of transferring relevant information from one individual or system to another to ensure continuity. It          │
│  requires clear, concise, and complete communication to avoid loss of critical information. Additionally, documentation and standardized handoff         │
│  protocols improve the reliability and durability of memory transfer between parties.                                                                    │
│                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
