# Spec Kit Workflow

This example is a compact adaptation of the workflow documented in `https://github.com/github/spec-kit`.

GitHub Spec Kit commonly includes `/speckit.constitution` near the start of a full project workflow to capture shared constraints. Chapter 9 keeps the example compact, so this walkthrough stays centered on the steps that define, plan, task, and implement the backlog-scoring change shown below.

The files in `artifacts/spec.md`, `artifacts/plan.md`, and `artifacts/tasks.md` are representative stand-ins for the fuller per-feature artifacts that Spec Kit normally manages.

## Representative Command Flow

```text
specify init .
/speckit.specify
/speckit.plan
/speckit.tasks
/speckit.implement
```

## Example Feature Request

Create an `idea-score` feature that lets a team score backlog ideas from `impact`, `effort`, and `strategic_fit` inputs so they can compare candidate work consistently.
