# Feature: Idea Scoring

## Description
As a product manager, I want to score backlog ideas based on impact, effort, and strategic fit so that the team can prioritize work objectively.

## Requirements

- Create an `Idea` model with fields: title (string), impact (0-5), effort (0-5), strategic_fit (0-5)
- Create a `score_idea` function that computes: `impact * 5 + strategic_fit * 3 - effort * 2`
- Raise `ValueError` if any numeric field is outside the 0-5 range
- Keep the model immutable

## Acceptance Criteria

1. An idea with impact=4, effort=2, strategic_fit=5 scores 31
2. An idea with impact=6 raises ValueError