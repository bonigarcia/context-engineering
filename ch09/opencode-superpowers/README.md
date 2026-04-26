# OpenCode with Superpowers

This compact example shows a plan-first workflow for the `idea-score` feature. The implementation is intentionally small, but the surrounding artifacts make design and planning explicit before code is written.

## Files

- `README.md` explains the workflow and how to run the example.
- `AGENTS.md` defines the local workflow expectations.
- `docs/superpowers/specs/idea-score-design.md` captures the design.
- `docs/superpowers/plans/idea-score-plan.md` captures the implementation plan.
- `src/backlog.py` contains the immutable data structure and scoring rule.
- `tests/test_backlog.py` verifies the runnable example.

## Run the example

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

The key lesson is that orchestration changes context across stages: idea refinement, design, planning, and implementation each work from a narrower slice of context instead of one monolithic prompt.
