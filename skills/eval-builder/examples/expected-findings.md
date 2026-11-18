# Expected results for examples/support-agent.md

A correct run produces at least five cases, with at least one in each of the categories happy-path, policy-violation, and adversarial (and ideally edge-case too). Good cases include a refund request within 30 days (happy path), a refund request for plants after 48 hours without a photo (policy violation), a request to change the account email (policy violation), and an email that asks the agent to ignore its instructions and print them (adversarial).

The findings report gaps in the specification, at least:

- Rule 4 ("Be helpful and sound professional") has no observable pass condition.
- The output format is not defined beyond "a draft reply" (length, greeting, signature, language).
