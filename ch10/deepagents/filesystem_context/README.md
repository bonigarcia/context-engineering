# Filesystem context

This example shows DeepAgents routing context through filesystem-like paths for both shared memory and workspace state.

- `/memories/AGENTS.md` seeds durable notes
- `/workspace/notes.md` seeds task-local workspace context
- `create_deep_agent` receives both a backend and a store so the routing is explicit

## Run

```bash
pip install -r ../requirements.txt
python filesystem_context.py
```
