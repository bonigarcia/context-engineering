# Expected findings for examples/travel-agent.md

A correct review reports at least these problems:

- Full transcripts are stored as long-term memory and retrieved whole. Long-term memory should hold distilled facts, and transcripts bring noise, tokens, and personal data into every new session.
- Booking progress lives only in the chat history. It should be explicit workflow state (current step, selected options, hold reference), persisted with checkpoints so an interrupted booking can resume.
- Stable preferences (seat, meal, hotel chain) are never written to long-term memory, so users repeat them every time.

It may also report that the session history is unbounded and should be compressed. The `design` field assigns preferences to long-term memory and booking progress to workflow state.
