# Phase 1 Research: Core Scoring Logic

## Findings
- Python `@dataclass(frozen=True)` enforces immutability out-of-the-box.
- Range checks can be added directly inside a custom scoring function or post-init verification.
- Unit tests can use `unittest.TestCase.assertRaisesRegex` to verify validation errors are raised with proper field-specific messages.
