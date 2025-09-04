# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    LLM_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"

settings = Settings()
