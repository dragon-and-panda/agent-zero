from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    marketing_rag_endpoint: AnyHttpUrl | None = None

    vision_api_base: AnyHttpUrl | None = None
    vision_api_key: str | None = None

    craigslist_email: str | None = None
    mercari_api_key: str | None = None

    websocket_origin_whitelist: List[str] = []

    class Config:
        env_prefix = "ALS_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
