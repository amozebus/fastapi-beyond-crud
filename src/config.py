"""Config for .env variables"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Model for .env variables validation"""

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int

    JTI_BLOCKLIST_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
