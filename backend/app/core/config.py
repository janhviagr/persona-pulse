from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite+aiosqlite:///./personapulse.db"
    GEMINI_API_KEY: str = ""
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000"
    DEFAULT_PERSONA_COUNT: int = 20
    MAX_PERSONA_COUNT: int = 500
    MAX_CONCURRENT_AGENTS: int = 10


settings = Settings()
