# Expected findings for examples/classify-ticket.txt

A correct review reports at least these problems:

- All five examples belong to the billing category. Shipping, technical, and account have no example, which biases the model toward billing.
- The examples use two different formats (`Ticket:` and `Category: billing` against `Input: "..."` and `Output -> BILLING`, with different casing). The model may copy either one.
- The prompt does not define the output format the code expects, or what to answer when no category fits.

It may also report that the categories have no definitions, that the ticket variable is not delimited, and that there is no borderline example. The review includes a revised prompt.
