# app/core/config.py
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    MONGODB_URL: str = Field(..., env="MONGODB_URL")
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()