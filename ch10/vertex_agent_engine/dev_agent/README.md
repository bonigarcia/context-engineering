# Development Agent with Vertex AI Agent Engine

This example deploys a software development agent built with the [Agent Development Kit](https://google.github.io/adk-docs/) to the managed runtime of [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview). The agent reads a feature spec, generates implementation code, and writes tests—all within a single managed session.

The agent definition stays portable, and only the deployment call is specific to the service. The managed runtime provides session isolation and memory across turns.

## Requirements

- [Python](https://www.python.org/) 3.10+
- A Google Cloud project with the Vertex AI API enabled
- Application Default Credentials configured (`gcloud auth application-default login`)
- A Cloud Storage bucket used for staging

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

2. Export the project settings as environment variables:
```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export STAGING_BUCKET="gs://your-staging-bucket"
```

3. Run the script:
```bash
python dev_agent.py
```

## Output

The script creates a remote agent in the managed runtime and streams the agent's reasoning and tool calls as it reads `spec.md`, generates the implementation, and writes the test file. Deployment takes several minutes the first time, and the resulting agent remains available until deleted.

> Note: deploying to a managed runtime creates billable cloud resources. The spec file `spec.md` in this folder is a sample you can modify to test different feature descriptions.