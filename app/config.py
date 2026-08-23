from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise RAG Accelerator"
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: str = "mock-key"
    LLM_DEPLOYMENT_NAME: str = "gpt-4o"
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    RATE_LIMIT_PER_MINUTE: str = "20/minute"

    class Config:
        case_sensitive = True

settings = Settings()


