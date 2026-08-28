# SDD with Spec Kit

This compact example uses [Spec Kit](https://github.com/github/spec-kit) as a staged workflow for a small backlog assistant that computes idea scores from `impact`, `effort`, and `strategic_fit` inputs.

The files in `artifacts/spec.md`, `artifacts/plan.md`, and `artifacts/tasks.md` are representative stand-ins for the fuller per-feature artifacts that Spec Kit normally manages.

## Representative Command Flow

```text
specify init .
/speckit.constitution
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.tasks
/speckit.analyze
/speckit.implement
```

`/speckit.clarify` and `/speckit.analyze` are optional in Spec Kit, but both are included here because they are where ambiguity is removed. `clarify` asks targeted questions about the underspecified parts of the spec and records the answers in `artifacts/spec.md`. `analyze` cross-checks the spec, the plan, and the task list for gaps and contradictions before any code is written.

## Example Feature Request

Create an `idea-score` feature that lets a team score backlog ideas from `impact`, `effort`, and `strategic_fit` inputs so they can compare candidate work consistently.

## Run the Example Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

The compact artifacts in this directory keep the workflow small while still showing how the backlog-scoring request becomes a spec, a plan, and an executable task list. In a full Spec Kit project, those artifacts are typically managed per feature rather than as one shared `artifacts/` folder.
