# Idea Score Design

## Goal

Add a compact `idea-score` function to a backlog assistant.

## Constraints

- Keep the example instructional and minimal.
- Accept only integer score components between 0 and 5 inclusive.
- Return a deterministic integer score.

## Formula

Use `impact * 5 + strategic_fit * 3 - effort * 2`.
