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
❌ Performs AI reasoning
❌ Knows about MCP response format
❌ Knows about SigNoz response format

Architecture
------------
AlertAgent
      ↓
AlertTool
      ↓
TelemetryService
      ↓
SigNoz
===============================================================================
"""

from __future__ import annotations

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
            description="Retrieves active alerts.",
        ) 

        self.telemetry = TelemetryService()
        
    # -------------------------------------------------------------------------
    # Retrieve Alerts
    # -------------------------------------------------------------------------

    async def execute(
        self,
        **kwargs,
    ) -> list[Alert]:
        """
        Retrieve active alerts.
        """

        self.log(
            "Retrieving active alerts."
        )

        alerts = await self.telemetry.get_alerts(
            **kwargs,
        )

        self.log(
            f"Retrieved {len(alerts)} alert(s)."
        )

        return alerts

    # -------------------------------------------------------------------------
    # Health Check
    # -------------------------------------------------------------------------

    async def health_check(
        self,
    ) -> bool:
        """
        Verify telemetry connectivity.
        """

        return await self.telemetry.health_check()