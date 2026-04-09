from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

print(BASE_DIR)

class Settings(BaseSettings):
    # for PostgreSQL
    db_host: str
    db_port: int
    db_name: str
    postgres_user: str
    postgres_password: str
    max_connection_count: int = 10

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")


settings = Settings()
