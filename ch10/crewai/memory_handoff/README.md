# Memory Handoff

This example shows CrewAI memory in action: one task records notes and the next task reuses them as context.

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
