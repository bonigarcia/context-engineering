# Architecture Document

## Technical Decisions
- **Stack**: Standard Python libraries (dataclasses, unittest).
- **Data Model**: Python frozen dataclass (`Idea`) to guarantee immutability.
- **Validation**: Strict boundary check (0-5 inclusive) inside `score_idea` to catch numeric domain violations.
- **Scoring**: Weighted score computation function `score_idea`.
