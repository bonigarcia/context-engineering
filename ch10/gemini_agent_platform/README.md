# Gemini Enterprise Agent Platform examples

This folder contains examples demonstrating how an agent is hosted on the Agent Runtime of [Gemini Enterprise Agent Platform](https://cloud.google.com/products/gemini-enterprise-agent-platform), the Google Cloud platform known as Vertex AI until April 2026. The Agent Runtime component was previously called Vertex AI Agent Engine, and the Python client still exposes it through the `agent_engines` module inherited from the earlier naming.

## Requirements

- [Python](https://www.python.org/) 3.10+
- A Google Cloud project with the Gemini Enterprise Agent Platform API (`aiplatform.googleapis.com`) enabled and Application Default Credentials configured

## Examples

- `deploy_adk_agent/`: Deploying an Agent Development Kit agent to the managed runtime and querying it.
- `dev_agent/`: A development agent that reads a spec and generates implementation code with tests.

## Running the examples

Each example is in its own folder and contains a `README.md` with instructions on how to run it.
