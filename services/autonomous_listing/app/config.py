from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    marketing_rag_endpoint: AnyHttpUrl | None = None

    vision_api_base: AnyHttpUrl | None = None
    vision_api_key: str | None = None

    craigslist_email: str | None = None
    mercari_api_key: str | None = None

    # --- Persistence ---
    db_path: str = "/workspace/tmp/autonomous_listing.db"

    # --- Autopublish (opt-in; use with caution) ---
    autopublish_enabled: bool = False
    autopublish_acknowledge_risk: bool = False
    playwright_headless: bool = True
    playwright_storage_state_path: str | None = None
    craigslist_base_url: AnyHttpUrl | None = None  # e.g. https://minneapolis.craigslist.org

    websocket_origin_whitelist: List[str] = []

    class Config:
        env_prefix = "ALS_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
