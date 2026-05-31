# ADK state example

This example demonstrates how to manage and update session state within an ADK application. It showcases two primary methods for state modification:
1.  Using `output_key` in an `LlmAgent` to automatically save the agent's final text response to a specified state key.
2.  Manually constructing `state_delta` within `EventActions` for more complex state updates, including those with `user:` and `temp:` prefixes.

## Requirements

* [Python](https://www.python.org/) 3.10+
* A [Google API key](https://ai.google.dev/) set as an environment variable (`GOOGLE_API_KEY`)

## Steps for running this example in the shell

1. Install dependencies:
```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Export your API key as an environment variable:
```bash
export GOOGLE_API_KEY="sk-..." # Windows cmd: set GOOGLE_API_KEY="sk-..." # Windows PowerShell: $env:GOOGLE_API_KEY="sk-..."
```

3. Run the script:
```bash
python state_example.py
```

## Output

The script will execute two scenarios:
 
* Greeting Agent: An `LlmAgent` with `output_key` configured will generate a greeting, and its response will be automatically saved to the session state.
* Manual State Update: Explicit `EventActions` will be used to update `task_status`, `user:login_count`, and `user:last_login_ts` in the session state.

The script will print the initial and updated states of the sessions, demonstrating how state changes are recorded and persisted.

Example output (simplified):

```
--- Running GreetingAgent (output_key) Example ---
Initial state: {'user:login_count': 0, 'task_status': 'idle'}
Agent responded with: "Hello there! How can I help you today?"
State after agent run: last_greeting = "Hello there! How can I help you today?"

--- Running Manual State Update (EventActions) Example ---
Initial state: {'user:login_count': 0, 'task_status': 'idle'}
`append_event` called with explicit state delta.
State after event: task_status='active', user:login_count=1, user:last_login_ts=<timestamp>
As expected, temp state was not persisted: 'temp:validation_needed' not found.
```
