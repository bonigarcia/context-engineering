# DSPy

This Chapter 10 bucket shows how DSPy expresses tasks as signatures and runs them through modules with a local deterministic LM.

## Runnable examples

- `ticket_triage/`: support-ticket triage with structured outputs.
- `structured_output/`: a compact action-plan generator with typed fields.
- `context_tooling/`: a local retrieval tool that threads offline context into the answer step.
- `stepwise_reasoning/`: a reasoned reply pattern with separate reasoning and answer fields.

## Run

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r ch10/dspy/<example>/requirements.txt
   ```
3. Run the example:
   ```bash
   python ch10/dspy/<example>/<example>.py
   ```
