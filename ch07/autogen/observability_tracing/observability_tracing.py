import autogen
import os
import logging

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from autogen.core import SingleThreadedAgentRuntime
from autogen.agentchat import AssistantAgent
from autogen.agentchat.contrib.user_proxy_agent import UserProxyAgent

# Configure OpenTelemetry
resource = Resource.create(attributes={"service.name": "autogen-example"})
provider = TracerProvider(resource=resource)
processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Enable AutoGen's telemetry
# This environment variable needs to be set to 'true' for AutoGen to emit telemetry events
os.environ["AUTOGEN_ENABLE_EXPERIMENTAL_TELEMETRY"] = "true"

# Configuration for the models
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

# Create agents within a runtime that supports telemetry
# Pass the configured trace_provider to the runtime
runtime = SingleThreadedAgentRuntime(trace_provider=provider)

assistant = AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. Respond with 'TERMINATE' when the task is done.",
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
)

# Initiate chat with tracing enabled
print("Initiating chat with OpenTelemetry tracing enabled...")
user_proxy.initiate_chat(
    assistant,
    message="Tell me a short story about a brave knight.",
    runtime=runtime # Pass the runtime to enable tracing
)

print("OpenTelemetry traces should be visible in the console output above.")
