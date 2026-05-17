# Chapter 5 JavaScript examples

This folder contains JavaScript ports of the easier Chapter 5 examples.

## Examples

- `session_state_chat/` - transient structured session state
- `workflow_state_handoff/` - shared workflow state between planner and executor
- `mem0_chat/` - Mem0-backed long-term memory chat

## Run

Each example is its own Node project:

```bash
cd session_state_chat && npm install && npm start
cd ../workflow_state_handoff && npm install && npm start
cd ../mem0_chat && npm install && npm start
```
