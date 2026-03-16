from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_path: str = "/workspace/tmp/ethical_financial_system.db"

    class Config:
        env_prefix = "EFS_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
