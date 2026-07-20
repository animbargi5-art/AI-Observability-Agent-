from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Tattva AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    SIGNOZ_URL: str
    SIGNOZ_API_KEY: str = ""

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()