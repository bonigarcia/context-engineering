# DeepAgents

This chapter slice demonstrates the upstream `langchain-ai/deepagents` harness patterns.

## Included examples

- `research_harness`: repo/docs research with bounded notes and a DeepAgents planner
- `file_context`: selecting repo/docs files and trimming context into short notes
- `planning_loop`: a bounded multi-pass planning loop over those notes
- `human_approval`: an approval checkpoint before publishing the brief
- `filesystem_context`: filesystem-backed context and memory using DeepAgents backends
- `subagent_delegation`: parent agent delegating to isolated sub-agents

The examples are intentionally small and local. They keep context bounded and show the DeepAgents controls that matter in practice.
