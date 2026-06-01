# Memory and state

This example shows how a small local state object can remember one fact and answer a follow-up prompt deterministically.

## Prerequisites

- Python 3.10+
- `pytest` from this folder's `requirements.txt`

## Files to inspect first

- `memory_state_notes.md`: the exact prompts and expected topic value.
- `memory_state_config.md`: the minimal local-file setup notes.
- `semantic_kernel_memory_state.py`: the runnable example and helper functions.

## Configure

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Read `memory_state_config.md` and keep the example folder writable so `memory_state.json` can be created.

## Run

1. Run `python semantic_kernel_memory_state.py` from this folder.
2. The script will remember the prompt `Remember that my favorite topic is semantic kernels.` if the state file is empty.
3. It will then answer `What is my favorite topic?` from the saved state.

## Expected result

- `memory_state.json` appears in this folder.
- The stored topic is `semantic kernels`.
- The script prints the remembered topic and then `semantic kernels`.

## Cleanup or reset

1. Delete `memory_state.json` to reset the example.
2. Remove any virtual environment or cache files you created.
