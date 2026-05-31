# Planner Executor

This example shows a two-agent CrewAI flow where the planner creates a short plan and the executor receives it as context.

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
python planner_executor.py
```

## Output
The script will print the planner's plan and the executor's final answer to the console.

```
╭────────────────────────────────────────────────────────────── 🔍 Execution Trace Generated ──────────────────────────────────────────────────────────────╮
│                                                                                                                                                          │
│  🎉 Your First CrewAI Execution Trace is Ready!                                                                                                          │
│                                                                                                                                                          │
│  View your execution details here:                                                                                                                       │
│  https://app.crewai.com/crewai_plus/ephemeral_trace_batches/588ad385-f863-49e3-aca6-3902069e92b7?access_code=TRACE-45ddd17a62                            │
│                                                                                                                                                          │
│  This trace shows:                                                                                                                                       │
│  • Agent decisions and interactions                                                                                                                      │
│  • Task execution timeline                                                                                                                               │
│  • Tool usage and results                                                                                                                                │
│  • LLM calls and responses                                                                                                                               │
│                                                                                                                                                          │
│  ✅ Tracing has been enabled for future runs!                                                                                                            │
│  Your preference has been saved. Future Crew/Flow executions will automatically collect traces.                                                          │
│                                                                                                                                                          │
│  To disable tracing later, do any one of these:                                                                                                          │
│  • Set tracing=False in your Crew/Flow code                                                                                                              │
│  • Set CREWAI_TRACING_ENABLED=false in your project's .env file                                                                                          │
│  • Run: crewai traces disable                                                                                                                            │
│                                                                                                                                                          │
│  📝 Note: This link will expire in 24 hours.                                                                                                             │
│                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
