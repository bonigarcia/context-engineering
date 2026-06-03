# Antigravity with Open GSD

This compact example shows how an existing coding agent can use Open GSD as the workflow layer for a small `idea-score` task. The artifact is documentation-first: the workflow lives in markdown instead of a custom Python harness.

## Files

- `README.md` explains the example and how to read the artifacts.
- `antigravity-workflow.md` captures the staged workflow and the ship gate.

## Representative workflow

```text
/gsd discuss
/gsd plan
/gsd execute
/gsd verify
/gsd ship
```

## Why this example exists

The point is to show that Open GSD can sit behind an existing coding agent and keep the execution loop explicit, verified, and auditable.
