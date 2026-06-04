# Phase 1 Context: Core Scoring Logic

## Decisions
- Model: Immutable Python `@dataclass`.
- Formula: `impact * 5 + strategic_fit * 3 - effort * 2`.
- Validation: Boundaries from 0 to 5 inclusive; raise `ValueError` on failure.
- Testing: Standard `unittest` framework.
