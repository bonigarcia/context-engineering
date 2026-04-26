from dataclasses import dataclass


@dataclass(frozen=True)
class Idea:
    title: str
    impact: int
    effort: int
    strategic_fit: int


def score_idea(idea: Idea) -> int:
    for field_name in ("impact", "effort", "strategic_fit"):
        value = getattr(idea, field_name)
        if type(value) is not int:
            raise ValueError(f"{field_name} must be an integer between 0 and 5")
        if not 0 <= value <= 5:
            raise ValueError(f"{field_name} must be between 0 and 5")

    return idea.impact * 5 + idea.strategic_fit * 3 - idea.effort * 2
