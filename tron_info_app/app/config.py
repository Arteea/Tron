from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str = "sqlite+aiosqlite:///./tron_info.db"
    TRON_NETWORK: str = "shasta"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings= Settings()