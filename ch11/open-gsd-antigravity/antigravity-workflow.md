# Antigravity workflow for idea-score

## Goal

Use Open GSD to turn the `idea-score` feature request into a verified change.

## Stage Pipeline

1. **Discuss (`/gsd-discuss-phase 1`)**: Align on requirements (REQ-001, REQ-002, REQ-003) and log choices in `.planning/phases/01-backlog-scoring/CONTEXT.md`.
2. **Plan (`/gsd-plan-phase 1`)**: Perform stack verification (`RESEARCH.md`) and compile atomic tasks (`01-01-PLAN.md`).
3. **Execute (`/gsd-execute-phase 1`)**: Implement core dataclass and scoring function in `src/backlog.py`.
4. **Verify (`/gsd-verify-work 1`)**: Run verification suite and compile UAT checks (`VERIFICATION.md`, `UAT.md`).
5. **Ship (`/gsd-ship 1`)**: Confirm all checks pass and merge/ship.

## Ship Gate Checklist

- [x] All requirements (REQ-001, REQ-002, REQ-003) verified.
- [x] Automated unit test suite passes.
- [x] Planning artifacts in `.planning/` updated and committed.
- [x] Git working tree is clean.
