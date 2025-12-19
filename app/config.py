# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    database_url: str = "sqlite:///./data/app.db"

    scrape_interval_seconds: int = 120

    telegram_bot_token: str = ""
    telegram_dry_run: bool = True


settings = Settings()
