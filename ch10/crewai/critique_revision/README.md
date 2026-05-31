# Critique Revision

This example shows a small review loop: one agent drafts, another critiques, and a third revises the answer.

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
python critique_revision.py
``

## Output
The script will print the initial draft, the critique, and the revised answer to the console.

```
╭──────────────────────────────────────────────────────────────────── Crew Completion ─────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                          │
│  Crew Execution Completed                                                                                                                                │
│  Name: crew                                                                                                                                              │
│  ID: 8739c627-8405-4b0a-9dd1-48144353b59e                                                                                                                │
│  Final Output: ```markdown                                                                                                                               │
│  **Context Handoff**                                                                                                                                     │
│                                                                                                                                                          │
│  Context handoff refers to the process of transferring relevant information, state, or situational awareness from one party or system to another to      │
│  ensure continuity and coherence. This technique is widely used across various fields such as customer service, software development, and multitasking   │
│  environments.                                                                                                                                           │
│                                                                                                                                                          │
│  For example, when a customer support ticket is escalated from a first-level representative to a specialist, a well-executed context handoff ensures     │
│  the specialist has all necessary background information to assist efficiently without requiring the customer to repeat details. Conversely, if this     │
│  handoff is done poorly—such as missing critical information—the specialist may ask the customer to reiterate their issue, causing frustration, delays,  │
│  and a poor customer experience. Similarly, in technical systems, failing to accurately transfer session data or process states between components can   │
│  lead to errors, disrupted workflows, or interrupted user experiences.                                                                                   │
│                                                                                                                                                          │
│  These real-world scenarios highlight why effective context handoff is essential. It minimizes information loss and reduces errors or delays caused by   │
│  miscommunication or missing data. Achieving this requires clear protocols, thorough documentation, and often automated tools that capture and transfer  │
│  the context accurately. Mastering context handoff thus plays a crucial role in maintaining workflow continuity, enhancing collaboration across teams    │
│  or systems, and ultimately ensuring seamless operations.                                                                                                │
│  ```                                                                                                                                                     │
│                                                                                                                                                          │
│                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```