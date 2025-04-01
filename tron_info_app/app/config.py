from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str = "sqlite:///./tron_info.db"
    TRON_NETWORK: str = "shasta"


    class Config:
        env_file: ".env"


settings= Settings()