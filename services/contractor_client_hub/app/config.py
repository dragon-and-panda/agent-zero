from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    threads_path: str = "/workspace/logs/contract_hub/threads.json"
    telemetry_path: str = "/workspace/logs/contract_hub/events.log"
    experience_memory_path: str = "/workspace/logs/contract_hub/experience_memory.json"
    rag_corpus_paths: List[str] = []
    platform_treasury_wallet: str = "0x000000000000000000000000000000000000dEaD"
    default_network: str = "polygon"
    default_token: str = "USDT"
    ai_arbiter_wallet: str = "0x000000000000000000000000000000000000aAaA"

    class Config:
        env_prefix = "CCH_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
