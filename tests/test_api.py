import json
from pathlib import Path

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


def test_analyze_rejects_blank_candidate_profile() -> None:
    response = client.post(
        "/analyze",
        json={
            "job_posting": "Need Python APIs.",
            "candidate_profile": "   ",
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


def test_sample_output_matches_mock_result() -> None:
    job_posting = Path("samples/job_posting.txt").read_text(encoding="utf-8")
    candidate_profile = Path("samples/candidate_profile.txt").read_text(encoding="utf-8")
    expected = json.loads(Path("samples/sample_output.json").read_text(encoding="utf-8"))

    result = analyze_fit(job_posting, candidate_profile)

    assert result.model_dump() == expected


def test_sample_mock_output_uses_concrete_portfolio_guidance() -> None:
    job_posting = Path("samples/job_posting.txt").read_text(encoding="utf-8")
    candidate_profile = Path("samples/candidate_profile.txt").read_text(encoding="utf-8")

    result = analyze_fit(job_posting, candidate_profile)
    evidence_text = " ".join(strength.evidence for strength in result.strengths)
    plan_text = " ".join(item.action for item in result.preparation_plan)

    assert "typed API responses" in evidence_text
    assert "pytest tests" in evidence_text
    assert "Streamlit demo" in plan_text
    assert "non-technical reviewer" in plan_text
