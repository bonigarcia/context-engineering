# ADK state example

This example demonstrates how to manage and update session state within an ADK application. It showcases two primary methods for state modification:
1.  Using `output_key` in an `LlmAgent` to automatically save the agent's final text response to a specified state key.
2.  Manually constructing `state_delta` within `EventActions` for more complex state updates, including those with `user:` and `temp:` prefixes.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
   Ensure your Google API key (`GOOGLE_API_KEY`) is set as an environment variable.

3. Run the script:
```bash
python state_example.py
```

## Expected Output
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