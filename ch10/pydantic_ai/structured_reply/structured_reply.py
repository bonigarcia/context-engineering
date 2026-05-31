"""Deterministic structured output example for Pydantic AI."""

from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel


class ReplySummary(BaseModel):
    category: Literal["billing", "bug", "account"] = Field(
        description="The ticket category"
    )
    confidence: float = Field(description="Confidence score from 0 to 1", ge=0, le=1)
    summary: str = Field(description="Short structured summary")


reply_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=ReplySummary,
    instructions="Return a concise, structured summary of the support request.",
)


def main() -> None:
    with reply_agent.override(
        model=TestModel(
            custom_output_args={
                "category": "bug",
                "confidence": 0.94,
                "summary": "The customer reports an export failure in the app.",
            }
        )
    ):
        result = reply_agent.run_sync(
            "The app fails when I export my invoice as PDF."
        )

    print(result.output.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
