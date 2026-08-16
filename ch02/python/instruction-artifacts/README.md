# Instruction artifacts

This folder contains examples of instruction artifacts, which are files that store project-specific or environment-specific directives for AI agents.

## Examples

- `task-tracker/`: A sample Python project demonstrating the use of portable and agent-specific instruction artifacts:
    - `AGENTS.md`: Portable Markdown format for coding-agent guidance.
    - `CLAUDE.md`: Anthropic's convention for Claude Code.

## Purpose

Instruction artifacts transform implicit team or project instructions into explicit agent-readable guidance. They reduce repetition, improve consistency across sessions, and make it easier to align agent behavior with the norms of a specific environment.

For more details on how to use these files with different AI agents, refer to the artifact adapters inside the `task-tracker` folder.
