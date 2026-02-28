from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Jarvis Ultra"
    app_env: str = "dev"
    log_level: str = "INFO"
    google_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    max_context_messages: int = 12
    data_dir: str = "./data"
    tts_provider: str = "edge"
    ada_voice_name: str = "en-US-AvaMultilingualNeural"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
