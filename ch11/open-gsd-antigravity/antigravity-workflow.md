# Antigravity workflow for idea-score

## Goal

Use Open GSD to turn a small backlog-scoring request into a verified change.

## Workflow

1. Discuss the request and confirm the scope.
2. Plan the change and write the stage artifacts.
3. Execute the minimal code change.
4. Verify with unit tests and review the git diff.
5. Ship only when the work is verified and the history is clean.

## Ship gate

- The tests pass.
- The plan artifact is up to date.
- The git working tree is clean.
