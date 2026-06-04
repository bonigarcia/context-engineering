# Specialized Agents with the BMAD Method

This example demonstrates multi-agent orchestration through role decomposition using the [BMAD Method](https://docs.bmad-method.org/) framework. Each specialized agent (Product Manager, Architect, Developer, Reviewer) is given a focused role file containing a small, specific slice of context. This isolation makes execution and verification much more reliable than using a single monolithic context.

## Folder Structure

The directory is organized following the official BMAD installation structure:

- `_bmad/` holds configuration and agent profiles:
  - `_bmad/agents/product-manager.md` (Role description for PM)
  - `_bmad/agents/architect.md` (Role description for Architect)
  - `_bmad/agents/developer.md` (Role description for Developer)
  - `_bmad/agents/reviewer.md` (Role description for Reviewer)
- `_bmad-output/` holds generated planning and implementation artifacts:
  - `_bmad-output/planning-artifacts/PRD.md` (Requirements document)
  - `_bmad-output/planning-artifacts/architecture.md` (Technical design decisions)
  - `_bmad-output/planning-artifacts/epics/epic-01-core-scoring.md` (Epic and story definitions)
  - `_bmad-output/implementation-artifacts/sprint-status.yaml` (Active sprint status tracking)
- `src/backlog.py` contains the implemented backlog prioritization module.
- `tests/test_backlog.py` contains the verification unit test suite.

## Run the example

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
