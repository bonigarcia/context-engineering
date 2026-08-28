# idea-score Spec

This compact file is a representative stand-in for the fuller per-feature `spec.md` artifact that Spec Kit normally manages.

## Feature

The `idea-score` feature calculates a compact priority score for a backlog idea so teams can compare candidate work consistently.

## Inputs

- `title`: descriptive name for the idea
- `impact`: integer from `0` to `5`
- `effort`: integer from `0` to `5`
- `strategic_fit`: integer from `0` to `5`

## Scoring Rule

Use this formula:

`impact * 5 + strategic_fit * 3 - effort * 2`

## Clarifications

Recorded from the `/speckit.clarify` step:

- Are non-integer numeric inputs such as `4.0` accepted? No. Only the `int` type is valid, so `4.0` is rejected.
- Can the final score be negative? Yes. A high-effort, low-impact idea can score below zero, and that result is kept as is.
- What happens on invalid input? A `ValueError` is raised naming the first failing field, and no score is returned.

## Acceptance Criteria

- The feature returns the weighted score for valid inputs.
- `impact`, `effort`, and `strategic_fit` must be integers only.
- Any score field outside the `0` to `5` range is rejected.
- Invalid integer type or out-of-range input raises `ValueError` and names the failing field.
