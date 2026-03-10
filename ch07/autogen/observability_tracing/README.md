# Observability and Tracing with AutoGen and OpenTelemetry

This example demonstrates how to integrate OpenTelemetry with an AutoGen application to gain observability into agent interactions, LLM calls, and tool executions. By configuring a `TracerProvider` and a `SpanProcessor`, you can collect and export detailed traces, which are invaluable for debugging complex multi-agent workflows and performance analysis.

## Requirements

*   [Python](https://www.python.org/) 3.8+
*   An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Steps for running this example

1.  Install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2.  Set environment variables:
    Ensure your OpenAI API key is set as an environment variable. Also, enable AutoGen's experimental telemetry:
    ```
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    AUTOGEN_ENABLE_EXPERIMENTAL_TELEMETRY="true"
    ```

3.  Run the script:
    ```bash
    python observability_tracing.py
    ```

## Expected Output

When the script runs, OpenTelemetry will capture traces of the agent's actions, including the LLM calls made during the conversation. These traces will be exported to the console (as configured with `ConsoleSpanExporter`), providing a detailed log of the events and their duration. Look for output similar to the following, which indicates spans for agent creation and invocation, and LLM calls.

```text
Initiating chat with OpenTelemetry tracing enabled...
user_proxy (to assistant):

Tell me a short story about a brave knight.
--------------------------------------------------------------------------------
INFO:opentelemetry.sdk.trace:Span finished: name="create_agent", kind=<SpanKind.INTERNAL: 0>, status=Ok, attributes={'gen_ai.agent.name': 'assistant', 'gen_ai.agent.id': 'assistant', 'gen_ai.system': 'autogen'}
INFO:opentelemetry.sdk.trace:Span finished: name="invoke_agent", kind=<SpanKind.INTERNAL: 0>, status=Ok, attributes={'gen_ai.agent.name': 'assistant', 'gen_ai.agent.id': 'assistant', 'gen_ai.system': 'autogen'}
INFO:opentelemetry.sdk.trace:Span finished: name="chat", kind=<SpanKind.CLIENT: 2>, status=Ok, attributes={'llm.vendor': 'OpenAI', 'llm.request.model': 'gpt-4', 'llm.response.model': 'gpt-4', ...}
assistant (to user_proxy):

Once upon a time, in a kingdom far away, lived Sir Reginald, a knight known not for his strength, but for his unwavering courage. One day, a fierce dragon threatened the kingdom. Sir Reginald, despite his fear, rode out to face it. He didn't fight with brute force, but with a clever plan, luring the dragon into a trap. The kingdom was saved, and Sir Reginald, the brave and clever knight, was hailed as a hero. TERMINATE

OpenTelemetry traces should be visible in the console output above.
```
The exact content of the story and the trace details will vary based on the LLM's response, but the presence of `Span finished: name="create_agent"`, `name="invoke_agent"`, and `name="chat"` indicates successful OpenTelemetry integration.