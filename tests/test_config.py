from app.config import get_settings


def test_settings_load_from_dotenv(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FITFLOW_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    tmp_path.joinpath(".env").write_text(
        "FITFLOW_LLM_PROVIDER=demo\nOPENAI_MODEL=test-model\n",
        encoding="utf-8",
    )

    try:
        get_settings.cache_clear()
        settings = get_settings()

        assert settings.llm_provider == "demo"
        assert settings.openai_model == "test-model"
    finally:
        get_settings.cache_clear()
