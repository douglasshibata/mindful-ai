from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MindfulAI"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./mindful_ai.db"
    SYNC_DATABASE_URL: Optional[str] = None

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # OpenAI & Clinical AI
    OPENAI_API_KEY: str = "dummy-key"
    CBT_MODEL_NAME: str = "gpt-4o"

    # Security & Encryption (32-byte urlsafe base64 key or hex)
    DATA_ENCRYPTION_KEY: str = "dGVzdF9lbmNyeXB0aW9uX2tleV8zMl9ieXRlc19sb25nCg=="
    SECRET_KEY: str = "mindful_default_jwt_secret_key_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings()
