import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STRIPE_PUBLIC_KEY: str
    STRIPE_SECRET_KEY: str
    BASE_URL: str = "http://localhost:8000"
    STRIPE_SUCCESS_URL: str
    STRIPE_CANCEL_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
