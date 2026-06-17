"""Deterministic tool-and-context example for Pydantic AI."""

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel


@dataclass
class SupportContext:
    team: str
    severity_threshold: int


class RoutingResult(BaseModel):
    route: Literal["billing", "support", "platform"] = Field(
        description="Where the ticket should go"
    )
    priority: Literal["low", "medium", "high"] = Field(
        description="Assigned priority"
    )
    note: str = Field(description="Short routing note")


routing_agent = Agent(
    "openai:gpt-5-mini",
    deps_type=SupportContext,
    output_type=RoutingResult,
    instructions=(
        "Route support tickets using the injected team context. Use the helper tool "
        "to check the severity threshold, then return structured output only."
    ),
)


@routing_agent.instructions
def add_context(ctx: RunContext[SupportContext]) -> str:
    return (
        f"Routing team: {ctx.deps.team}. "
        f"Severity threshold: {ctx.deps.severity_threshold}."
    )


@routing_agent.tool
def needs_escalation(ctx: RunContext[SupportContext], severity: int) -> bool:
    return severity >= ctx.deps.severity_threshold


def main() -> None:
    deps = SupportContext(team="support", severity_threshold=7)

    with routing_agent.override(
        model=TestModel(
            custom_output_args={
                "route": "support",
                "priority": "high",
                "note": "Escalate because the customer is blocked.",
            }
        )
    ):
        result = routing_agent.run_sync(
            "The customer cannot access their account after a failed payment.",
            deps=deps,
        )

    print(result.output.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
