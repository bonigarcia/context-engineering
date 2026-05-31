# Agno

This Chapter 10 bucket shows how Agno separates the agent runtime from the control plane.

The runnable example stays focused on a single workspace tool so you can see the agent inspect a scoped directory, while Agno's AgentOS framing explains how the same agent can later be stored, traced, and served as a managed service without changing the core agent logic.

## Runnable example

- `sorting_hat`: a workspace-scoped agent that inventories the local `ch10/agno` folder and groups what it finds.

## Companion notes

- `session_memory`: session history persists between runs.
- `knowledge_store`: knowledge sources become explicit context inputs.
- `agent_os_service`: the same agent runs as a service behind AgentOS.
- `audit_traces`: traces show which context reached each run.
