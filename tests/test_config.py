from pathlib import Path

from app import config
from app.config import get_settings


def test_settings_load_from_dotenv(monkeypatch) -> None:
    dotenv_path = Path(config.__file__).parents[1] / ".env"
    original_dotenv = dotenv_path.read_bytes() if dotenv_path.exists() else None

    monkeypatch.delenv("FITFLOW_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    try:
        dotenv_path.write_text(
            "FITFLOW_LLM_PROVIDER=demo\nOPENAI_MODEL=test-model\n",
            encoding="utf-8",
        )

        get_settings.cache_clear()
        settings = get_settings()

        assert settings.llm_provider == "demo"
        assert settings.openai_model == "test-model"
    finally:
        get_settings.cache_clear()
        if original_dotenv is None:
            dotenv_path.unlink(missing_ok=True)
        else:
            dotenv_path.write_bytes(original_dotenv)
