from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Tattva AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    SIGNOZ_URL: str
    SIGNOZ_SERVICE_ACCOUNT_KEY: str = ""

    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    OTEL_SERVICE_NAME: str = "tattva-ai-backend"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()