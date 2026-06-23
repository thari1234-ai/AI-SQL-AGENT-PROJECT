import json

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    secret_key: str = "dev-secret-change-me"
    access_token_expire_minutes: int = 60 * 24

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "ai_sql_agent"
    postgres_sslmode: str = ""

    sql_max_rows: int = 500
    sql_timeout_seconds: int = 15

    llm_provider: str = "mock"
    llm_api_key: str = ""
    llm_model: str = "gemini-2.0-flash"
    llm_temperature: float = 0.2

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    rate_limit_per_minute: int = 60
    auto_seed_demo_data: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if value is None:
            return ["http://localhost:3000"]

        if isinstance(value, list):
            return value

        if isinstance(value, str):
            raw = value.strip()
            if not raw:
                return ["http://localhost:3000"]

            if raw.startswith("["):
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except json.JSONDecodeError:
                    pass

            return [item.strip() for item in raw.split(",") if item.strip()]

        return ["http://localhost:3000"]

    @property
    def sqlalchemy_database_uri(self) -> str:
        base = (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
        if self.postgres_sslmode:
            return f"{base}?sslmode={self.postgres_sslmode}"
        return base


settings = Settings()
