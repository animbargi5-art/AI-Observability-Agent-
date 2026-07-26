"""
===============================================================================
TattvaAI - Alert Tool
===============================================================================

Purpose
-------
Provides normalized alert data for AI investigation agents.

Responsibilities
----------------
• Retrieve normalized alerts
• Hide TelemetryService implementation
• Return Alert domain models

This tool NEVER:
----------------
❌ Parses JSON
❌ Knows about MCP
❌ Knows about SigNoz response format
❌ Performs AI reasoning

Architecture
------------
AlertAgent
        ↓
AlertTool
        ↓
Application Telemetry Service
        ↓
SigNoz Telemetry Service
        ↓
MCP Gateway
        ↓
SigNoz

===============================================================================
"""

from __future__ import annotations

from app.core.logging import logger
from app.models.alert import Alert
from app.services.telemetry_service import TelemetryService
from app.tools.base_tool import BaseTool


class AlertTool(BaseTool):
    """
    Tool responsible for retrieving normalized alerts.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Alert Tool",
            description="Retrieves active alerts from SigNoz.",
        )

        self.telemetry = TelemetryService()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    async def execute(
        self,
    ) -> list[Alert]:
        """
        Retrieve active alerts.
        """

        logger.info(
            "AlertTool: Retrieving active alerts."
        )

        alerts = await self.telemetry.get_alerts()

        logger.info(
            "AlertTool: Retrieved %d alerts.",
            len(alerts),
        )

        return alerts

    async def health_check(self) -> bool:
        """
        Verify telemetry connectivity.
        """

        return await self.telemetry.health_check()