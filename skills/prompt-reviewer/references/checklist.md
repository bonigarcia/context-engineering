# Prompt review checklist

Each rule has a short rationale and the book section where the idea is explained.

## Task

1. The prompt states the task, the input, and the expected output in plain terms, early in the prompt. (Chapter 6, Core design principles)
2. Every label, category, or option the model can produce is defined, with a short criterion for each one. Undefined categories get used inconsistently. (Chapter 6, Core design principles)
3. Variables are clearly delimited (tags, fences, or headings), so user input cannot be confused with instructions. (Chapter 6, Production considerations)

## Few-shot examples

4. Examples cover every category or output type, in roughly balanced numbers. Examples that all share one label bias the model toward that label. (Chapter 6, Few-shot prompting)
5. All examples use exactly the same input and output format, the one the calling code expects. Mixed formats produce mixed outputs. (Chapter 6, Few-shot prompting)
6. Examples include at least one hard or borderline case, not only obvious ones. (Chapter 6, Few-shot prompting)
7. Examples are short and realistic, and do not repeat information that is already in the instructions. (Chapter 6, Few-shot prompting)

## Output

8. The output format is specified exactly (JSON schema, a single label, fixed fields), and the prompt says what to output when no option fits. Code that parses the output depends on this. (Chapter 6, Core design principles)
9. Structured output features of the API (JSON mode, schemas) are used when available, instead of relying on wording alone. (Chapter 6, Production considerations)

## Chains and techniques

10. In a prompt chain, each step has one job and passes only what the next step needs, in a defined format. (Chapter 6, Prompt chaining)
11. Step-by-step reasoning is requested only when the task needs it, and kept out of the final output when the output is parsed. Reasoning models need less of this. (Chapter 6, Prompting and reasoning models)
12. The prompt is versioned and tested on a fixed set of inputs before changes reach production. (Chapter 6, Production considerations)
