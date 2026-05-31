# Research harness

This runnable example follows the upstream DeepAgents pattern:

- `create_deep_agent` builds the agent
- local tools expose repo/docs research
- notes stay bounded before the final brief is produced

It keeps the example local and testable while still showing the long-horizon research shape.

## What it demonstrates

- A small set of local markdown helpers for repo/docs research
- Bounded notes so the harness does not carry every read forward
- A concise brief instead of a large context dump
- An upstream-style builder that can be monkeypatched in tests

## Run

```bash
pip install -r ../requirements.txt
python research_harness.py
```
