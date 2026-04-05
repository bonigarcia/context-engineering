# SDLC prompt library

This directory contains seven reusable prompts for different tasks across the software development lifecycle (SDLC).

The prompt set follows a mixed strategy:

- One primary prompt framework per role (10-step prompt structure, COSTAR, CRISPE, RTF, or BAB).
- A small number of complementary prompting techniques (role prompting, few-shot prompting, chain-of-thought prompting, tree-of-thought prompting, ReAct prompting, self-consistency prompting, prompt chaining, meta-prompting, or reflective prompting).
- Placeholders to be filled with specific context (`[...]`).

The seven prompts are:

1. [The architect](01_architect.md) (for planning and design).
2. [The developer](02_developer.md) (for code generation).
3. [The debugger](03_debugger.md) (for debugging).
4. [The reviewer](04_reviewer.md) (for code reviewing).
5. [The refactorer](05_refactorer.md) (for refactoring).
6. [The tester](06_tester.md) (for automated testing).
7. [The documenter](07_documenter.md) (for documentation).

These prompts are intended to be adapted to the target stack, repository conventions, and delivery environment. They are not magic formulas but reusable context containers for recurring software engineering work.