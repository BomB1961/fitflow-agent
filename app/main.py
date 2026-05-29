from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from app.config import get_settings
from app.models import FitAnalysisRequest, FitAnalysisResponse, HealthResponse
from app.service import analyze_fit

app = FastAPI(
    title="FitFlow Agent",
    description="MVP API for comparing a job posting with a candidate profile.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", provider=settings.llm_provider)


@app.post("/analyze", response_model=FitAnalysisResponse)
def analyze(request: FitAnalysisRequest) -> FitAnalysisResponse:
    try:
        return analyze_fit(request.job_posting, request.candidate_profile)
    except ValidationError as exc:
        raise HTTPException(status_code=502, detail="Provider returned invalid analysis output.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
