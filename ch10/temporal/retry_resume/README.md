# Temporal retry and resume

This companion explains the pattern where a transient failure interrupts an AI step, then Temporal retries it and resumes from durable workflow state.

The key idea is that the workflow keeps its progress in Temporal, so a retry does not rebuild the full context from scratch.
