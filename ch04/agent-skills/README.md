# Agent skills for CLI workflows

This folder contains an example of an [Agent Skill](https://agentskills.io/) used to guide a CLI-capable agent through a workspace analysis task.

## Example

- `workspace-analyzer/`: A skill that helps the agent inspect a project tree, identify temporary files, and perform only the approved cleanup or reorganization steps.

## Usage

Agent skills are loaded by compatible agents from their configured skills directory. In this chapter, the skill is used as procedural context that narrows how a terminal agent should explore and modify the workspace.
