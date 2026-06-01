# Planner and executor

This example shows a local Semantic Kernel process with two deterministic steps: a planner step that turns the request `Organize a three-step plan for a small day-of-week reminder workflow.` into a fixed three-step plan, and an executor step that runs those steps in order.

## Prerequisites

- Python 3.10+
- `semantic-kernel` and `pytest` installed from this folder's `requirements.txt`
- No API key or external chat-completion service is required

## Files to inspect first

- `planner_executor_plan.md`: the exact request string and the ordered workflow.
- `planner_executor_config.md`: the local setup notes for the process demo.
- `semantic_kernel_planner_executor.py`: the deterministic helpers, process steps, and `main()` entry point.
- `test_semantic_kernel_planner_executor.py`: the exact helper output assertions.

## Configure Semantic Kernel

1. Create and activate a Python virtual environment.
2. Install the dependencies from `requirements.txt`.
3. Read `planner_executor_config.md` and keep the example folder as the active workspace.
4. Read `planner_executor_plan.md` and confirm the exact request string is visible before you run anything.

## Run the example

1. Run `python semantic_kernel_planner_executor.py` from this folder.
2. Confirm the process prints a `Plan:` section with three numbered steps.
3. Confirm the process prints an `Execution:` section with the deterministic `done: ...` lines.

## Expected result

- The request is split into a short, readable plan.
- The executor runs those plan steps in order.
- The final output includes both `Plan:` and `Execution:` sections.

## Cleanup or reset

1. Remove any virtual environment or cache files you created.
