# Research and Write with CrewAI

This example shows the smallest useful CrewAI flow for context handoff: a researcher gathers facts and a writer uses that research to draft the final response.

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
python research_and_write.py
```

## Output

When you run the script, you should see output similar to the following in your terminal:

```
╭──────────────────────────────────────────────────────────────────── Crew Completion ─────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                          │
│  Crew Execution Completed                                                                                                                                │
│  Name: crew                                                                                                                                              │
│  ID: 6fdf69a5-f8a8-4b6f-ad55-d9cffe7b320c                                                                                                                │
│  Final Output: ```markdown                                                                                                                               │
│  # Summary of Context Engineering                                                                                                                        │
│                                                                                                                                                          │
│  Context engineering is the systematic design, creation, and management of context-aware systems that adapt their behavior based on environmental        │
│  conditions, user states, or situations. Its core purpose is to enable systems to understand and utilize contextual information—such as location, time,  │
│  user activity, device state, or social environment—to enhance functionality, personalization, and responsiveness.                                       │
│                                                                                                                                                          │
│  Context types include physical context (e.g., location, temperature), computational context (e.g., network status, device capabilities), user context   │
│  (e.g., preferences, emotional state), and environmental context (e.g., lighting, noise). The key components of context engineering are:                 │
│                                                                                                                                                          │
│  - **Context Acquisition:** Gathering contextual data via sensors and techniques.                                                                        │
│  - **Context Modeling:** Structuring context information using ontologies or data models.                                                                │
│  - **Context Reasoning:** Inferring higher-level context through rules, machine learning, or probabilistic methods.                                      │
│  - **Context Dissemination:** Sharing context data with relevant system parts.                                                                           │
│  - **Context Management:** Maintaining, updating, and ensuring privacy and consistency of context data.                                                  │
│                                                                                                                                                          │
│  Context engineering is widely applied in ubiquitous computing, smart environments, IoT devices, adaptive user interfaces, personalized and              │
│  location-based services. Challenges include handling heterogeneous data sources, ensuring data accuracy and freshness, managing privacy and security,   │
│  and coping with resource constraints on devices.                                                                                                        │
│                                                                                                                                                          │
│  Several tools and frameworks, such as Context Toolkit and OpenIoT, support context engineering by facilitating data integration and reasoning. Current  │
│  research focuses on improving inference accuracy, standardizing models, enhancing privacy-preserving methods, and employing AI for dynamic context      │
│  adaptation.                                                                                                                                             │
│  ```                                                                                                                                                     │
│                                                                                                                                                          │
│                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```