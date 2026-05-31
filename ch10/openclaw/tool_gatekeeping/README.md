# Tool gatekeeping

This example shows channel access and sandboxing as explicit control points.

The platform decides which senders are allowed, how DMs are paired, and what runs inside a sandbox.

Inspect `openclaw.json5`.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [OpenAI API key](https://platform.openai.com/api-keys) set as an environment variable (`OPENAI_API_KEY`)

## What it demonstrates

- Intercepting and authorizing tool execution.
