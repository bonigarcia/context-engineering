# Claude Code Agent Skills Example

This compact example shows how Claude Code can use [agent-skills](https://github.com/addyosmani/agent-skills) as the workflow layer for a tiny product backlog assistant with an `idea-score` feature. The public skill pack is the durable workflow artifact: it carries the reusable SDLC routine instead of relying on a one-off prompt.

The code stays intentionally small. The durable workflow context lives in the public agent-skills plugin and is reinforced by `CLAUDE.md` and `agent-skills-workflow.md`.

## Requirements

* [Claude Code](https://claude.com/product/claude-code)

## Steps for running this example

Start Claude Code from this folder so the local `CLAUDE.md`, `agent-skills-workflow.md`, `src/`, and `tests/` files are all in scope for the session.

If the public skill pack is not installed yet, install it inside Claude Code:

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
/reload-plugins
```

Then use the public `agent-skills` lifecycle commands. Some Claude Code installations expose the short aliases, while others expose the fully qualified command names. Use whichever form appears in your session.

```text
/spec
/plan
/build
/test
/review
```

Equivalent namespaced commands:

```text
/agent-skills:spec-driven-development
/agent-skills:planning-and-task-breakdown
/agent-skills:incremental-implementation
/agent-skills:test-driven-development
/agent-skills:code-review-and-quality
```

When the spec command asks what you want to build, reply with a short feature description such as:

```text
Add an idea-score capability to this backlog example. Use an immutable Idea model with title, impact, effort, and strategic_fit. Keep each numeric field between 0 and 5. Use the formula impact * 5 + strategic_fit * 3 - effort * 2. Keep the code minimal and verify with python -m unittest discover -s tests -p "test_*.py" -v.
```

After the workflow completes, or at any point when you want to verify the runnable example directly from the shell, run:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
