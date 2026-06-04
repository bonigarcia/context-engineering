# Project: Backlog Scoring Helper

## Overview
A lightweight module for a product backlog assistant that calculates a transparent prioritization score for backlog ideas.

## Scope
- Define an immutable `Idea` data structure.
- Define a scoring function `score_idea` applying the weighted formula `impact * 5 + strategic_fit * 3 - effort * 2`.
- Enforce validation boundaries on all score inputs (integers between 0 and 5).
