---
name: workspace-analyzer
description: Inspect a workspace, identify temporary files, and perform only approved cleanup or organization steps.
---

# Workspace Analyzer

## Instructions
1. Use `find` or the platform equivalent to locate temporary files such as `.tmp`, `.bak`, and editor backup files.
2. Run `git status --short` before making changes so tracked and untracked files are easy to distinguish.
3. Present the findings to the user and wait for confirmation before deleting or moving anything.
4. Delete only the approved files, then rerun the scan to verify the workspace is clean.
5. When reorganizing files, group them by extension into clearly named folders and report every move.
