# Specialized agents with the BMAD Method

This compact example shows how the small `idea-score` feature can be decomposed into narrower role artifacts instead of one broad prompt. Each role carries only the context needed for its handoff, and the Python files provide a runnable anchor.

## Files

- `README.md` explains the example and how to run it.
- `agents/product-manager.md` states the business intent for `idea-score`.
- `agents/architect.md` states the design boundary for the implementation.
- `agents/developer.md` states the implementation task and scoring formula.
- `agents/reviewer.md` contains the review checklist.
- `src/backlog.py` contains the immutable model and scoring function.
- `tests/test_backlog.py` verifies the runnable example.

## Run the example

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Role specialization reduces context sprawl and makes handoffs explicit, which is the main teaching point of this example.
