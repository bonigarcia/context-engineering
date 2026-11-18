# Evaluation design checklist

Each rule has a short rationale and the book section where the idea is explained.

## Coverage

1. Cases start from the specification: every "must" and "must never" rule gets at least one case that would fail if the rule were broken. (Chapter 8, Evals)
2. The set mixes happy paths, edge cases (empty, very long, ambiguous, or multilingual input), policy violations (input that tempts the system to break a rule), and adversarial input (prompt injection, requests to reveal instructions). (Chapter 8, Evaluation datasets)
3. Cases use realistic inputs, ideally taken or adapted from real traffic, and each case has a short description of what it checks. (Chapter 8, Evaluation datasets)

## Assertions

4. Deterministic assertions (`contains`, `not-contains`, `regex`, `is-json`, JSON schema) come first. They are cheap, fast, and do not vary between runs. (Chapter 8, Evaluation metrics)
5. Model-graded assertions (`llm-rubric`) are used for meaning that keywords cannot capture, with a rubric that states the pass condition in one or two concrete sentences. (Chapter 8, LLM-as-judge)
6. Each assertion checks one thing, so a failure points to one cause. (Chapter 8, Evals)
7. The judge model and its settings are fixed and stated, since a different judge gives different scores. (Chapter 8, LLM-as-judge)

## Gaps in the specification

8. When a rule has no observable pass condition ("be helpful", "sound professional"), report it as a gap and propose a testable version. (Chapter 8, Evals)
9. When the output format is undefined, report it as a gap, since format checks are the cheapest and most reliable assertions. (Chapter 8, Evaluation metrics)

## Use

10. The set is small enough to run on every prompt or model change, and it is run before and after each change to compare results. (Chapter 8, Evals)
11. Cases that fail in production are added to the set, so the same failure is caught next time. (Chapter 8, Evaluation datasets)
