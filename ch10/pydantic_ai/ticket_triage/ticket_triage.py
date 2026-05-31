"""Deterministic ticket triage example for Pydantic AI."""

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel


@dataclass
class TriageContext:
    queue_name: str


class TicketTriage(BaseModel):
    priority: Literal["low", "medium", "high"] = Field(
        description="Priority assigned to the ticket"
    )
    team: Literal["billing", "support", "platform"] = Field(
        description="Team that should handle the ticket"
    )
    reply: str = Field(description="Short response to the customer")


triage_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=TriageContext,
    output_type=TicketTriage,
    instructions=(
        "Triage incoming support tickets. Use the provided queue name, keep the "
        "response short, and return only structured output."
    ),
)


@triage_agent.instructions
def add_queue_context(ctx: RunContext[TriageContext]) -> str:
    return f"Current queue: {ctx.deps.queue_name}."


@triage_agent.tool
def is_billing_queue(ctx: RunContext[TriageContext]) -> bool:
    return ctx.deps.queue_name == "billing"


def main() -> None:
    deps = TriageContext(queue_name="billing")

    with triage_agent.override(model=TestModel(seed=0)):
        result = triage_agent.run_sync(
            "Customer cannot download an invoice after a payment failure.", deps=deps
        )

    print(result.output.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
