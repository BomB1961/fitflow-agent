import json
from abc import ABC, abstractmethod
from typing import Any
from urllib import request

from app.config import Settings


def _strip_json_code_fence(content: str) -> str:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


class LLMProvider(ABC):
    name: str

    @abstractmethod
    def analyze(self, job_posting: str, candidate_profile: str) -> dict[str, Any]:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    name = "mock"

    keyword_map = {
        "python": "Python",
        "fastapi": "FastAPI",
        "api": "API design",
        "pydantic": "Pydantic",
        "testing": "Testing",
        "pytest": "Testing",
        "llm": "LLM integration",
        "prompt": "Prompt design",
        "docker": "Docker",
        "sql": "SQL",
        "react": "React",
        "streamlit": "Streamlit",
    }

    def analyze(self, job_posting: str, candidate_profile: str) -> dict[str, Any]:
        job_lower = job_posting.lower()
        profile_lower = candidate_profile.lower()
        required_skills: dict[str, set[str]] = {}

        for token, label in self.keyword_map.items():
            if token in job_lower:
                required_skills.setdefault(label, set()).add(token)

        if not required_skills:
            required_skills = {
                "Role alignment": {"role"},
                "Project communication": {"communication"},
                "Learning plan": {"learning"},
            }

        matched = [
            skill
            for skill, tokens in required_skills.items()
            if any(token in profile_lower for token in tokens)
        ]
        missing = [skill for skill in required_skills if skill not in matched]

        if not matched:
            matched = ["Project communication"]
        if not missing:
            missing = ["Targeted role examples"]

        score = max(0, min(100, 35 + (len(matched) * 8) - (len(missing) * 7)))

        strengths = [
            {
                "skill": skill,
                "evidence": f"The candidate profile includes experience related to {skill}.",
            }
            for skill in matched[:4]
        ]
        gaps = [
            {
                "skill": skill,
                "importance": "high" if index == 0 else "medium",
                "why_it_matters": f"The job posting appears to value {skill}, but the profile does not show enough direct evidence.",
            }
            for index, skill in enumerate(missing[:4])
        ]
        plan = [
            {
                "priority": index + 1,
                "action": f"Prepare a concise portfolio example that demonstrates {gap['skill']}.",
                "reason": gap["why_it_matters"],
                "suggested_time": "2-4 hours",
            }
            for index, gap in enumerate(gaps)
        ]

        return {
            "fit_score": score,
            "summary": "The candidate shows partial alignment with the role and should focus preparation on the highest-impact gaps.",
            "rationale": "This deterministic demo compares role keywords with candidate evidence to produce a stable portfolio-friendly output.",
            "strengths": strengths,
            "missing_skills": gaps,
            "preparation_plan": plan,
            "provider": self.name,
        }


class OpenAICompatibleProvider(LLMProvider):
    name = "openai-compatible"

    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when FITFLOW_LLM_PROVIDER=openai.")
        self.settings = settings

    def analyze(self, job_posting: str, candidate_profile: str) -> dict[str, Any]:
        prompt = (
            "Analyze the fit between this job posting and candidate profile. "
            "Return only JSON with keys: fit_score, summary, rationale, strengths, "
            "missing_skills, preparation_plan, provider.\n\n"
            f"Job posting:\n{job_posting}\n\nCandidate profile:\n{candidate_profile}"
        )
        payload = {
            "model": self.settings.openai_model,
            "messages": [
                {"role": "system", "content": "You produce concise structured job-fit analysis JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        data = json.dumps(payload).encode("utf-8")
        endpoint = f"{self.settings.openai_base_url.rstrip('/')}/chat/completions"
        req = request.Request(
            endpoint,
            data=data,
            headers={
                "Authorization": f"Bearer {self.settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with request.urlopen(req, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))

        content = body["choices"][0]["message"]["content"]
        result = json.loads(_strip_json_code_fence(content))
        result["provider"] = self.name
        return result


def build_provider(settings: Settings) -> LLMProvider:
    if settings.llm_provider in {"mock", "demo"}:
        return MockLLMProvider()
    if settings.llm_provider in {"openai", "openai-compatible"}:
        return OpenAICompatibleProvider(settings)
    raise ValueError(f"Unsupported FITFLOW_LLM_PROVIDER: {settings.llm_provider}")
