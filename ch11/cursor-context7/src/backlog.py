from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class Idea(BaseModel):
    title: str
    impact: int = Field(..., ge=0, le=5)
    effort: int = Field(..., ge=0, le=5)
    strategic_fit: int = Field(..., ge=0, le=5)


class IdeaResponse(BaseModel):
    title: str
    impact: int
    effort: int
    strategic_fit: int
    score: int


def score_idea(idea: Idea) -> int:
    if not (0 <= idea.impact <= 5 and 0 <= idea.effort <= 5 and 0 <= idea.strategic_fit <= 5):
        raise ValueError("Scores must be between 0 and 5")
    return idea.impact * 5 + idea.strategic_fit * 3 - idea.effort * 2


@app.post("/score", response_model=IdeaResponse)
def score_idea_endpoint(idea: Idea) -> IdeaResponse:
    try:
        score = score_idea(idea)
        return IdeaResponse(
            title=idea.title,
            impact=idea.impact,
            effort=idea.effort,
            strategic_fit=idea.strategic_fit,
            score=score,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
