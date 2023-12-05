from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'SPPU-RESULT-CONVERTER'
    UPLOADCARE_API_KEY: str
    DROPBOX_ACCESS_TOKEN: str
    WEBSITE_DOMAIN: str = 'http://localhost:8000'
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAILS_ENABLED: bool = False
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_LOGIN: str
    SMTP_PASSWORD: str
    SMTP_API_KEY: str
    EMAILS_FROM_NAME: str
    EMAILS_FROM_EMAIL: str
    EMAIL_TEMPLATES_DIR: str = "/fastApiProject/internal/email-templates/build"
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
