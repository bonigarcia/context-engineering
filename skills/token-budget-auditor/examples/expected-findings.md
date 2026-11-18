# Expected findings for examples/context

The sample context has four files: `system-prompt.md` (instructions), `tools.json` (tools), `retrieved.md` (knowledge), and `history.md` (memory). The token budget in `budget.txt` is 6,000 tokens, and the script estimates about 7,400 tokens in total, so the context is over budget.

A correct audit reports at least these problems:

- The context is over the 6,000-token budget.
- `retrieved.md` contains the same returns-policy chunk three times. Deduplicate before assembly.
- `history.md` passes 40 exchanges verbatim, with the same questions repeated. Summarize or trim older turns.

It may also report that `system-prompt.md` repeats the same ten rules in eight sections (the largest source, about 2,700 tokens), and that twelve tools are loaded for every message, with near-identical generic descriptions. The token table must match the script output.
