# SDD with Spec Kit

This compact example shows [GitHub Spec Kit](https://github.com/github/spec-kit) as a staged workflow for a small backlog assistant that computes idea scores from `impact`, `effort`, and `strategic_fit` inputs.

In fuller Spec Kit setups, teams commonly add `/speckit.constitution` early to capture shared project rules. Chapter 11 keeps this example focused on the workflow that defines, plans, and implements the backlog-scoring change, so the walkthrough starts at specification and follows the main feature commands only.

## Files

- `README.md` explains the compact workflow and how to run the example.
- `spec-kit-workflow.md` shows the representative Spec Kit command flow for this example.
- `artifacts/spec.md` is a compact stand-in for the fuller per-feature spec artifact that Spec Kit normally manages.
- `artifacts/plan.md` is a compact stand-in for the fuller per-feature plan artifact that Spec Kit normally manages.
- `artifacts/tasks.md` is a compact stand-in for the fuller per-feature task artifact that Spec Kit normally manages.
- `src/backlog.py` contains the immutable data structure and scoring rule.
- `tests/test_backlog.py` verifies valid scoring and invalid input handling.

## Representative Command Flow

```text
specify init .
/speckit.specify
/speckit.plan
/speckit.tasks
/speckit.implement
```

## Run the Example Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

The compact artifacts in this directory keep the workflow small while still showing how the backlog-scoring request becomes a spec, a plan, and an executable task list. In a full Spec Kit project, those artifacts are typically managed per feature rather than as one shared `artifacts/` folder.
