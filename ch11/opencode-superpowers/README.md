# OpenCode with Superpowers

This example shows how to use the [Superpowers framework](https://github.com/obra/superpowers) with the [OpenCode.ai](https://opencode.ai) coding agent. Rather than "vibe coding" (jumping straight from user request to code), Superpowers enforces a structured, design-first engineering workflow.

## Installation in OpenCode

To give the OpenCode agent superpowers, add it to the `plugin` array in your project-level or global `opencode.json`:

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"]
}
```

Restart OpenCode to install the plugin. Verify that it was successfully registered by asking:
> "Tell me about your superpowers"

## Design-First Workflow

When you ask the agent to implement a feature (e.g., the `idea-score` feature), the workflow automatically moves through the following stages:

1. Socratic design (brainstorming):
   The agent utilizes the `superpowers/brainstorming` skill. It halts coding, discusses the requirements, and asks clarifying questions. The approved design is saved as a durable spec file in `docs/superpowers/specs/idea-score-design.md`.
2. Implementation planning:
   Once the spec is confirmed, the agent uses the `superpowers/writing-plans` skill to generate an implementation plan in `docs/superpowers/plans/idea-score-plan.md`, detailing the steps to execute.
3. Execution & Test-Driven Development (TDD):
   The agent executes the plan using the `superpowers/test-driven-development` skill. It writes failing unit tests first, implements the minimal code required to make them pass, and runs verification checks.

## File Structure

- `opencode.json` specifies the plugin configuration for OpenCode.
- `AGENTS.md` defines local workflow rules.
- `docs/superpowers/specs/idea-score-design.md` holds the design spec written during the brainstorming phase.
- `docs/superpowers/plans/idea-score-plan.md` holds the implementation plan detailing coding steps.
- `src/backlog.py` contains the final implemented code.
- `tests/test_backlog.py` contains unit tests checking the implementation.

## Local Verification

Run the unit tests to verify the example:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
