# Antigravity with Open GSD

This example demonstrates how the Antigravity coding agent integrates with the [Open GSD](https://www.opengsd.net/) (Git Ship Done) workflow layer. Instead of executing code changes in a single ad-hoc step, Open GSD enforces a structured lifecycle of planning, execution, verification, and shipping, preserving the execution log as inspectable Markdown files in the repository.

## Workflow Phases

Open GSD executes through the following commands (or equivalent namespace routers):

1. Initialization (`/gsd-new-project`): Discussion of project details and creation of project-level files (`PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`).
2. Discussion (`/gsd-discuss-phase <N>`): Confirms implementation details and choices for the active phase, writing them to `CONTEXT.md`.
3. Planning (`/gsd-plan-phase <N>`): Researches stack constraints and generates atomic task plan files (e.g., `01-01-PLAN.md`).
4. Execution (`/gsd-execute-phase <N>`): Executes plans in parallel, applies code changes, and updates phase summaries.
5. Verification (`/gsd-verify-work <N>`): Verifies requirements against checks, generating verification and UAT logs.
6. Shipping (`/gsd-ship <N>`): Gates completion with tests, plan checks, and git history cleanliness before building the final PR.

## Files

- `README.md` explains the example structure.
- `antigravity-workflow.md` captures the staged pipeline checklist.
- `src/backlog.py` implements the `Idea` model and scoring function.
- `tests/test_backlog.py` implements the verification unit tests.
- `.planning/` holds all Open GSD execution trace documents:
  - `PROJECT.md` (Project description)
  - `REQUIREMENTS.md` (Target requirement IDs)
  - `ROADMAP.md` (Phased roadmap status)
  - `STATE.md` (Current phase session memory)
  - `phases/01-backlog-scoring/` contains:
    - `CONTEXT.md` (Design and library selections)
    - `RESEARCH.md` (Stack research facts)
    - `01-01-PLAN.md` (XML structured task specification)
    - `01-01-SUMMARY.md` (Implementation outcome details)
    - `VERIFICATION.md` (Requirement verification checks)
    - `UAT.md` (Manual user acceptance checks)

## Local Verification

Run the unit test checks:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
