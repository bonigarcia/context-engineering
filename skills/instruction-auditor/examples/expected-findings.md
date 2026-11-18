# Expected findings for examples/AGENTS.md

A correct audit reports at least these problems:

- Contradiction: "Indent with tabs" in Code style conflicts with "Use 2-space indentation" in Formatting.
- Vague rule: "Write clean, high-quality code" cannot be checked. The fix names concrete criteria or a linter.
- Misplaced procedure: the 15-step release procedure in "Releasing a new version" is only needed for releases. It belongs in a skill (or a release script) that loads on demand.
- Unenforceable rule: "Never make mistakes" adds tokens without changing behavior.

The audit may also suggest enforcing formatting with a formatter configuration instead of prose. It must not report problems in the Build commands section, which is concrete and correct.
