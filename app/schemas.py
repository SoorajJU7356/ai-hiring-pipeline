from pydantic import BaseModel, Field


class ScoreReport(BaseModel):
    domain_relevance_score: int = Field(ge=0, le=10)
    experience_score: int = Field(ge=0, le=10)
    skills_match_score: int = Field(ge=0, le=10)
    weighted_score: float = Field(ge=0, le=100)
    reasoning: str
    matched_skills: list[str]
    skill_gaps: list[str]