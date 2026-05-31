# DeepAgents

This chapter slice shows a minimal DeepAgents-style pattern for long-horizon work.

## Included examples

- `research_harness`: runnable repo/docs research with bounded context
- `file_context`: how file reads are trimmed into compact notes
- `subagent_delegation`: how work would be split across helpers
- `planning_loop`: how a long task is revisited in stages
- `human_approval`: where a checkpoint would pause for review

The runnable example is intentionally small and local: it inspects a few repo/docs files, keeps only a bounded note buffer, reduces that into a `context_state`, and writes a concise brief.
