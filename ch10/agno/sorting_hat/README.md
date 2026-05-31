# Sorting Hat

This example uses Agno's real `Agent` and `Workspace` APIs to inspect the local `ch10/agno` directory.

The important part is the boundary: the agent only gets read-style workspace access, so it can inventory the folder without seeing the rest of the repository. That makes it a good fit for Agno's runtime/control-plane model, where the same agent can later be managed, traced, and served through AgentOS.

## Run

1. Install the dependencies from `requirements.txt`.
2. Set `OPENAI_API_KEY`.
3. Run `python sorting_hat.py`.

## What it shows

- Scoped workspace access to local files.
- A single agent that reasons over its own project folder.
- A clear path from ad-hoc script to managed AgentOS service.
