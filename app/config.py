from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    database_url: str
    app_name: str = "BLS Economic Data API"
    app_debug: bool = False
    log_level: str = "INFO"
    api_keys: str = ""


@lru_cache()
def get_settings() -> Settings:
    return Settings()
