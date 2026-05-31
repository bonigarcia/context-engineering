# Temporal examples

This folder contains examples demonstrating orchestrating resilient agent workflows using Temporal.

## Requirements

- [Python](https://www.python.org/) 3.10+
- A [Temporal Server](https://docs.temporal.io/cli) instance running locally

## Examples

- `retry_resume/`: Automatic retry policy handling network errors.
- `waiting_signal/`: Pausing workflow until a user signal is received.
- `durable_state/`: Preserving state over hours, days, or weeks of workflow execution.
- `human_approval/`: Human intervention workflow approval gateways.
- `subworkflow_boundary/`: Breaking execution into independent subworkflows.

## Running the examples

Each example is in its own folder and contains a `README.md` with instructions on how to run it.
