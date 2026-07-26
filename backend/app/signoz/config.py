"""
===============================================================================
TattvaAI - SigNoz Configuration
===============================================================================

This module centralizes all SigNoz-related configuration.

Responsibilities
----------------
• Read SigNoz configuration from the application settings
• Build HTTP headers
• Expose timeout and retry configuration
• Provide a single configuration interface for all SigNoz services

Configuration values are loaded from:

    app.core.settings

This module MUST NOT:

• Read .env directly
• Perform HTTP requests
• Execute MCP calls
• Contain business logic

===============================================================================
"""

from app.core.settings import settings


class SigNozConfig:
    """
    Central configuration used by every SigNoz service.
    """

    # =========================================================================
    # SigNoz Instance
    # =========================================================================

    SIGNOZ_URL: str = settings.SIGNOZ_URL

    # =========================================================================
    # MCP Server
    # =========================================================================

    MCP_SERVER_URL: str = settings.SIGNOZ_MCP_SERVER

    # =========================================================================
    # Authentication
    # =========================================================================

    API_KEY: str = settings.SIGNOZ_API_KEY

    # =========================================================================
    # Communication
    # =========================================================================

    REQUEST_TIMEOUT: int = 30

    MAX_RETRIES: int = 3

    VERIFY_SSL: bool = False

    # =========================================================================
    # Investigation Defaults
    # =========================================================================

    DEFAULT_TIME_RANGE: str = "30m"

    DEFAULT_TRACE_LIMIT: int = 100

    DEFAULT_LOG_LIMIT: int = 500

    DEFAULT_METRIC_LIMIT: int = 500

    DEFAULT_ALERT_LIMIT: int = 100

    # =========================================================================
    # Headers
    # =========================================================================

    @classmethod
    def headers(cls) -> dict[str, str]:
        """
        Build default headers for SigNoz requests.
        """

        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if cls.API_KEY:
            headers["SIGNOZ-API-KEY"] = cls.API_KEY

        return headers

    # =========================================================================
    # Base Configuration
    # =========================================================================

    @classmethod
    def base_config(cls) -> dict:
        """
        Return the default configuration shared by all SigNoz services.
        """

        return {
            "base_url": cls.SIGNOZ_URL,
            "timeout": cls.REQUEST_TIMEOUT,
            "verify_ssl": cls.VERIFY_SSL,
            "max_retries": cls.MAX_RETRIES,
            "headers": cls.headers(),
        }

    # =========================================================================
    # MCP Configuration
    # =========================================================================

    @classmethod
    def mcp_config(cls) -> dict:
        """
        Return MCP server configuration.
        """

        return {
            "server_url": cls.MCP_SERVER_URL,
            "timeout": cls.REQUEST_TIMEOUT,
            "headers": cls.headers(),
        }