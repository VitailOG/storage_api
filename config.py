from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    BASE_DIR: Path = Path(__file__).resolve().parent

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    @property
    def db_connection_string(self):
        dsn = PostgresDsn.build(
            scheme="postgres",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )
        return str(dsn)


settings = Settings()
