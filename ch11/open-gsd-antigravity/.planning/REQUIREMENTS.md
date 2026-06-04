# Requirements

- **REQ-001**: Implement an immutable `Idea` data structure containing `title` (string), `impact` (integer), `effort` (integer), and `strategic_fit` (integer).
- **REQ-002**: Inputs `impact`, `effort`, and `strategic_fit` must be integers between 0 and 5 inclusive. Any out-of-range value must raise a `ValueError`.
- **REQ-003**: Calculate the score using the formula `impact * 5 + strategic_fit * 3 - effort * 2`.
