from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    UPLOADCARE_API_KEY: str
    DROPBOX_ACCESS_TOKEN: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache
def get_settings():
    return Settings()
