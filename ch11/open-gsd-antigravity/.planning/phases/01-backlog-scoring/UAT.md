# Phase 1 User Acceptance Testing (UAT)

1. Can you construct an `Idea` object and verify it's immutable?
   - Response: Yes, attempting to write to `idea.impact` raises `dataclasses.FrozenInstanceError`. (Verified)

2. Does providing out-of-range values raise a `ValueError`?
   - Response: Yes, calling `score_idea` with `impact=6` raises `ValueError: impact must be between 0 and 5`. (Verified)

3. Does a valid input return the correct priority score?
   - Response: Yes, inputting `impact=4`, `effort=2`, `strategic_fit=5` yields `31`. (Verified)
