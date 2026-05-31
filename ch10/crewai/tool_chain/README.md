# Tool Chain

This example shows a small CrewAI workflow where an agent uses explicit tools to gather context before a writer drafts the answer.

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
python tool_chain.py
```

## Output

When you run the script, you should see output similar to the following in your terminal:

```
╭──────────────────────────────────────────────────────────────────── Crew Completion ─────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                          │
│  Crew Execution Completed                                                                                                                                │
│  Name: crew                                                                                                                                              │
│  ID: cb6c4bfa-8f86-4a19-bab9-ef7071e6a65e                                                                                                                │
│  Final Output: A tool chain is a set of programming tools used together to perform a complex software development task. It typically includes a          │
│  compiler, linker, debugger, and other utilities that transform source code into executable programs. Keeping the scope small helps maintain focus and   │
│  efficiency when using or developing tool chains.                                                                                                        │
│                                                                                                                                                          │
│                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

