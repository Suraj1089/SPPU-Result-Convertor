from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    PROJECT_NAME: str = 'fastapi-tutorials'
    DROPBOX_ACCESS_TOKEN: str
    DATABASE_URI: str = "postgresql://fastapi:fastapi@localhost/test"  # use local database in development
    WEBSITE_DOMAIN: str = 'http://localhost:8000'
    SECRET_KEY: str
    ALGORITHM: str
    EMAILS_ENABLED: bool = False
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_LOGIN: str
    SMTP_PASSWORD: str
    SMTP_API_KEY: str
    EMAILS_FROM_NAME: str
    EMAILS_FROM_EMAIL: str
    EMAIL_TEMPLATES_DIR: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
