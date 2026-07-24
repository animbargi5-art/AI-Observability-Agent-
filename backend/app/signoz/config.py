import os

from dotenv import load_dotenv

load_dotenv()


class SignozConfig:

    """
    Central configuration for all SigNoz integrations.
    """

    # ------------------------
    # MCP Server
    # ------------------------

    MCP_SERVER_URL = os.getenv(
        "SIGNOZ_MCP_SERVER",
        "http://localhost:8080"
    )

    # ------------------------
    # SigNoz Instance
    # ------------------------

    SIGNOZ_URL = os.getenv(
        "SIGNOZ_URL",
        "http://localhost:3301"
    )

    # ------------------------
    # Authentication
    # ------------------------

    API_KEY = os.getenv(
        "SIGNOZ_API_KEY",
        ""
    )

    # ------------------------
    # Communication
    # ------------------------

    REQUEST_TIMEOUT = 30

    MAX_RETRIES = 3

    VERIFY_SSL = False

    # ------------------------
    # Default Investigation Window
    # ------------------------

    DEFAULT_TIME_RANGE = "30m"

    # ------------------------
    # Headers
    # ------------------------

    @classmethod
    def headers(cls):

        headers = {}

        if cls.API_KEY:

            headers["SIGNOZ-API-KEY"] = cls.API_KEY

        if cls.SIGNOZ_URL:

            headers["X-SigNoz-URL"] = cls.SIGNOZ_URL

        return headers