"""Config for .env variables"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Model for .env variables validation"""

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_USER_PASSWORD: str

    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE: int  # minutes
    REFRESH_TOKEN_EXPIRE: int  # days

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
