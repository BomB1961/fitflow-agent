from fastapi.testclient import TestClient

from app.main import app
from app.service import analyze_fit


client = TestClient(app)


def test_health_uses_mock_provider_by_default() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "provider": "mock"}


def test_analyze_returns_structured_response() -> None:
    response = client.post(
        "/analyze",
        json={
            "job_posting": "Need Python, FastAPI, LLM prompt design, and pytest testing.",
            "candidate_profile": "Built Python FastAPI APIs with pytest tests.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["fit_score"] <= 100
    assert body["summary"]
    assert body["rationale"]
    assert body["strengths"]
    assert body["missing_skills"]
    assert body["preparation_plan"]
    assert body["provider"] == "mock"


def test_analyze_rejects_blank_job_posting() -> None:
    response = client.post(
        "/analyze",
        json={
            "job_posting": "   ",
            "candidate_profile": "Built Python APIs.",
        },
    )

    assert response.status_code == 422


def test_demo_mode_does_not_require_api_key() -> None:
    result = analyze_fit(
        "Need Python FastAPI LLM prompt design.",
        "Built Python and FastAPI portfolio projects.",
    )

    assert result.provider == "mock"
    assert result.preparation_plan
