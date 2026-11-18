# Evaluation harness for the skills

Running these evaluations requires an `OPENROUTER_API_KEY` environment variable, and every run calls a paid model.

This folder uses [Promptfoo](https://github.com/promptfoo/promptfoo) to check that each skill finds the problems it should find in its sample artifact, and that the skill descriptions make an agent pick the right skill. The approach follows the Promptfoo example of Chapter 8 of the book ([ch08/evals-promptfoo](../../ch08/evals-promptfoo)).

## Requirements

- [Node.js](https://nodejs.org/) (Promptfoo runs with `npx`)
- Python 3.10 or later (the prompt functions and assertions are Python)
- An [OpenRouter](https://openrouter.ai/) API key

## Running the evaluations

From this folder:

```bash
export OPENROUTER_API_KEY="sk-or-..."

# Behavior tests: one or more cases per skill
npx promptfoo@latest eval -c promptfooconfig.yaml

# Only the cases of one skill
npx promptfoo@latest eval -c promptfooconfig.yaml --filter-pattern tool-reviewer

# Activation tests: does the description select the right skill?
npx promptfoo@latest eval -c activation.yaml

# Optional: browse the results
npx promptfoo@latest view
```

The default model is `openai/gpt-6-luna` through OpenRouter, with temperature 0. The same model grades the `llm-rubric` assertions. To call OpenAI directly instead, replace `openrouter:openai/gpt-6-luna` with `openai:chat:gpt-6-luna` in both config files and set `OPENAI_API_KEY`.

## What the harness checks

- Behavior tests (`promptfooconfig.yaml`, cases in `cases/`). For each case, `prompt.py` builds a system message with the skill's `SKILL.md` body and its `references/` files, and a user message with the request and the sample artifacts from the skill's `examples/` folder. The model's report must end with a JSON block. `assertions.py` then checks that the block is valid, that every finding has a valid severity, that the required findings are present, that the forbidden ones are absent, and that skill-specific fields have the expected values. An `llm-rubric` assertion checks the findings that cannot be matched by keywords.
- Activation tests (`activation.yaml`, cases in `activation-cases.yaml`). The model receives the name and description of every skill and a user request, and must answer with the right skill name or with `none`. These tests exercise the `description` field, which is the only part of a skill an agent sees before loading it.
- Script tests. The scripts inside the skills have their own unit tests, which need no model:

```bash
python3 ../skill-reviewer/scripts/test_validate_frontmatter.py
python3 ../token-budget-auditor/scripts/test_count_tokens.py
python3 -m unittest discover -s tests
python3 -m unittest discover -s ../_tools/tests
```

## Known limits

The behavior tests simulate an agent that has already activated the skill. They do not exercise real activation inside an agent, on-demand file loading, or script execution. When a skill relies on a script, the case passes the script output in the request. Running the skills inside a real headless agent is out of scope for this harness.

## Adding a case

Add a file to `cases/` (or a test to an existing one) with these vars:

| Var | Meaning |
|---|---|
| `skill` | Skill directory name |
| `artifacts` | File or folder under the skill's `examples/` folder (several as a comma-separated string, since Promptfoo expands list vars into separate tests) |
| `request` | The user request |
| `required` | Findings that must appear. Each item has `keywords` (all must appear, `a\|b` means either) and an optional `location` substring |
| `forbidden` | Findings that must not appear, same format |
| `extra` | Top-level JSON fields with an exact expected value |
