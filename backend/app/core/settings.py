from pydantic_settings import (BaseSettings, SettingsConfigDict,)


class Settings(BaseSettings):
    APP_NAME: str = "Tattva AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    SIGNOZ_URL: str = ""
    SIGNOZ_API_KEY: str = ""
    SIGNOZ_MCP_SERVER: str = ""

    # Allows the product demo and local UI to run without a SigNoz account.
    # Production deployments must explicitly set this to false.
    DEMO_MODE: bool = False

    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    OTEL_SERVICE_NAME: str = "tattva-ai-backend"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    model_config  = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()
