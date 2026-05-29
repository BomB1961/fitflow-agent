from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from pydantic import BaseModel


class Settings(BaseModel):
    llm_provider: str = "mock"
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"


@lru_cache
def get_settings() -> Settings:
    load_dotenv()
    return Settings(
        llm_provider=getenv("FITFLOW_LLM_PROVIDER", "mock").strip().lower() or "mock",
        openai_api_key=getenv("OPENAI_API_KEY"),
        openai_base_url=getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        openai_model=getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )
