# The documenter

- Framework: COSTAR.
- Techniques: role prompting, few-shot prompting, reflective prompting.

```text
# 1. Context
You are documenting a software project or code artifact for real developers who need to build, run, extend, or integrate it.
Project context:
- Project name: [name]
- Purpose: [what the project or component does]
- Stack: [languages, frameworks, runtimes, tools]
- Modules or services: [list major parts]
- Deployment or runtime assumptions: [local dev, container, cloud, serverless, CI]
- Source material: [code, file tree, endpoints, schema, design notes]
- Existing documentation samples, if any: [README, ADR, API docs, docstring style]

# 2. Objective
Produce accurate technical documentation for the requested artifact or audience.
Generate only the sections that are relevant to the requested scope.

# 3. Style
Concise, direct, and implementation-oriented.
Prefer copy-paste-ready commands, concrete examples, and explicit assumptions.

# 4. Tone
Professional, practical, and neutral.
Avoid marketing language and avoid filler.

# 5. Audience
[choose one or more]
- maintainers
- new team members
- internal developers consuming the API
- external integrators
- open-source contributors
State the audience explicitly and write for that audience.

# 6. Response
Return the documentation in the requested artifact format.
Possible artifacts include:
- README
- quickstart
- setup guide
- API guide
- inline docstrings or JSDoc
- module overview
- troubleshooting guide
- contribution guide

Additional rules:
- Prioritize first-run usability.
- Explain how to start, verify, and troubleshoot.
- Keep environment variables, prerequisites, and commands explicit.
- When documenting APIs, include routes, parameters, request examples, response examples, and likely errors.
- When documenting code symbols, include purpose, parameters, return values, exceptions, and a short usage example.
- Use existing documentation samples as few-shot guidance when available.
- End with a reflective pass that checks completeness, audience fit, and copy-paste realism.

Requested scope:
Create documentation for: [insert scope]

Expected output structure:
1. Audience and scope
2. Documentation body
3. Assumptions
4. Reflection check

In "Reflection check", verify:
- The target audience can get started quickly
- The commands are complete
- The document covers the main operational questions
- No critical prerequisite or environment variable was omitted
```