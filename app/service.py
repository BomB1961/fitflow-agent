from app.config import get_settings
from app.models import FitAnalysisResponse
from app.providers import LLMProvider, build_provider


def get_provider() -> LLMProvider:
    return build_provider(get_settings())


def analyze_fit(
    job_posting: str,
    candidate_profile: str,
    provider: LLMProvider | None = None,
) -> FitAnalysisResponse:
    active_provider = provider or get_provider()
    raw_result = active_provider.analyze(job_posting, candidate_profile)
    return FitAnalysisResponse.model_validate(raw_result)
