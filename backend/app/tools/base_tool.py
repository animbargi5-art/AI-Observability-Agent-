"""
===============================================================================
TattvaAI - Base Tool
===============================================================================

Base class for all telemetry tools.

Responsibilities
----------------
• Shared logger
• Shared TelemetryService
• Shared AlertService
• Standard health check
• Common validation helpers
• Common exception handling

This class is provider-independent.

===============================================================================
"""

from __future__ import annotations

from typing import Any

from app.core.logger import logger

from app.signoz.telemetry_service import TelemetryService
from app.signoz.alert_service import AlertService
from app.signoz.documentation_service import DocumentationService


class BaseTool:
    """
    Base class for every Tool.
    """

    def __init__(self) -> None:

        self.logger = logger

    # ---------------------------------------------------------------------
    # Logging
    # ---------------------------------------------------------------------

    def log(
        self,
        message: str,
    ) -> None:

        self.logger.info(message)

    # ---------------------------------------------------------------------
    # Validation
    # ---------------------------------------------------------------------

    @staticmethod
    def validate_string(value: str | None) -> bool:

        return bool(
            value
            and value.strip()
        )

    @staticmethod
    def validate_payload(
        payload: dict[str, Any] | None,
    ) -> bool:

        return payload is not None

    # ---------------------------------------------------------------------
    # Health
    # ---------------------------------------------------------------------

    async def health(self) -> dict:

        return {

            "tool": self.__class__.__name__,

            "status": "ready"

        }

    # ---------------------------------------------------------------------
    # Error Handling
    # ---------------------------------------------------------------------

    def handle_error(
        self,
        exc: Exception,
    ) -> None:

        self.logger.exception(exc)

        raise exc