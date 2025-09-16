from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_NAME: str

    SECRET_JWT_KEY: str
    ALGORITHM_JWT: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_URL: str = "redis://localhost:6379/0"

    SMPT_HOST: str
    SMPT_PORT: str
    SMPT_USER: str
    SMTP_PASS: str

    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["INFO", "DEBUG", "ERROR", "WARNING"]

    class Config:
        env_file = ".env"


settings = Settings()
