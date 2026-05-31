# DeepAgents

This chapter slice shows a minimal DeepAgents-style pattern for long-horizon work.

## Included examples

- `research_harness`: runnable repo/docs research with bounded context
- `file_context`: runnable file reads trimmed into compact notes
- `subagent_delegation`: runnable delegation split across helpers
- `planning_loop`: runnable long task revisited in stages
- `human_approval`: runnable checkpoint that pauses for review

The runnable examples are intentionally small and local: they inspect a few repo/docs files, keep only bounded note buffers, reduce that into a `context_state`, and write concise briefs.
