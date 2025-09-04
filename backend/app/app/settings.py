from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    OPENAI_API_KEY: str | None = None
    LLM_MODEL: str = "gpt-4"
    EMBEDDINGS_MODEL: str = "text-embedding-3-small"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
