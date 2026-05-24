# LLM evals with Promptfoo

This example uses [Promptfoo](https://github.com/promptfoo/promptfoo) to compare two support-reply prompts on the same test set. It combines deterministic assertions with an `llm-rubric` judge so you can compare prompt quality directly.

## Requirements

This example requires [Node.js](https://nodejs.org/) and an OpenAI API key.

## Steps for running this example

1. Set your API key:
```bash
export OPENAI_API_KEY="sk-..."
```

2. Run the evaluation:
```bash
npx promptfoo@latest eval -c promptfooconfig.yaml
```

3. Optional: open the web viewer:
```bash
npx promptfoo@latest view
```

## Output

Promptfoo prints a comparison matrix for both prompt variants and shows the model-graded and deterministic scores for each test case.

```
Running 4 test cases (up to 4 at a time)...

┌────────────────────────────────────┬────────────────────────────────────┬────────────────────────────────────┬────────────────────────────────────┐
│ policy                             │ ticket                             │ [openai:chat:gpt-4o-mini]          │ [openai:chat:gpt-4o-mini]          │
│                                    │                                    │ support-reply-baseline.txt: You    │ support-reply-guardrailed.txt: You │
│                                    │                                    │ are a support assistant.           │ are a support assistant.           │
│                                    │                                    │ Use only the policy to answer the  │ Use only the policy to answer the  │
│                                    │                                    │ ticket.                            │ ticket.                            │
│                                    │                                    │ If the policy is insufficient, say │ Do not promise refunds or account  │
│                                    │                                    │ that a human review is needed.     │ changes unless the policy          │
│                                    │                                    │ Ticket:                            │ explicitly allows it.              │
│                                    │                                    │ {{ticket}}                         │ Ticket:                            │
│                                    │                                    │ Policy:                            │ {{ticket}}                         │
│                                    │                                    │ {{policy}}                         │ Policy:                            │
│                                    │                                    │ Write a concis...                  │ {{polic...                         │
├────────────────────────────────────┼────────────────────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ Duplicate charges must be          │ I was charged twice for order      │ [FAIL] Thank you for reaching out. │ [PASS] Thank you for reaching out. │
│ acknowledged, escalated to         │                                    │ Your duplicate charge will be      │ I will escalate your concern       │
│ billing, and verified before a     │                                    │ escalated to billing for           │ regarding the duplicate charges to │
│ refund is promised.                │                                    │ verification, and a human review   │ our billing team for verification. │
│                                    │                                    │ will be conducted to address your  │                                    │
│                                    │                                    │ concern.                           │                                    │
├────────────────────────────────────┼────────────────────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ Ask the user to request a fresh    │ My password reset link expired     │ [PASS] Please request a fresh      │ [PASS] Please request a fresh      │
│ reset link and avoid claiming the  │ before I could use it.             │ password reset link, as expired    │ password reset link to proceed     │
│ account was restored.              │                                    │ links cannot be reused. If you     │ with resetting your password.      │
│                                    │                                    │ need further assistance, a human   │                                    │
│                                    │                                    │ review may be necessary.           │                                    │
└────────────────────────────────────┴────────────────────────────────────┴────────────────────────────────────┴────────────────────────────────────┘
✓ Eval complete

Total Tokens: 1,433
  Eval: 402 (308 prompt, 94 completion)
  Grading: 1,031 (886 prompt, 145 completion)

Results:
  ✓ 3 passed (75.00%)
  ✗ 1 failed (25.00%)
  0 errors (0%)
Duration: 3s (concurrency: 4)
```

![Promptfoo UI](/docs/img/promptfoo-ui.png)
