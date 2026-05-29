from typing import Literal

from pydantic import BaseModel, Field, field_validator


class FitAnalysisRequest(BaseModel):
    job_posting: str = Field(..., min_length=1)
    candidate_profile: str = Field(..., min_length=1)

    @field_validator("job_posting", "candidate_profile")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Text input must not be blank.")
        return cleaned


class Strength(BaseModel):
    skill: str
    evidence: str


class MissingSkill(BaseModel):
    skill: str
    importance: Literal["high", "medium", "low"]
    why_it_matters: str


class PreparationPlanItem(BaseModel):
    priority: int = Field(..., ge=1)
    action: str
    reason: str
    suggested_time: str


class FitAnalysisResponse(BaseModel):
    fit_score: int = Field(..., ge=0, le=100)
    summary: str
    rationale: str
    strengths: list[Strength]
    missing_skills: list[MissingSkill]
    preparation_plan: list[PreparationPlanItem]
    provider: str = "mock"


class HealthResponse(BaseModel):
    status: str
    provider: str
