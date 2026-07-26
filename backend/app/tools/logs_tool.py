"""
===============================================================================
TattvaAI - Logs Tool
===============================================================================

Purpose
-------
Provides normalized log data for AI investigation agents.

Responsibilities
----------------
• Retrieve normalized logs
• Hide TelemetryService implementation
• Return Log domain models

This tool NEVER:
----------------
❌ Performs AI reasoning
❌ Knows about MCP
❌ Knows about SigNoz response format

Architecture
------------
LogsAgent
      ↓
LogsTool
      ↓
TelemetryService
      ↓
SigNoz
===============================================================================
"""

from __future__ import annotations

from app.models.log import Log
from app.services.telemetry_service import TelemetryService
from app.tools.base_tool import BaseTool


class LogsTool(BaseTool):
    """
    Tool responsible for retrieving normalized logs.
    """

    def __init__(self) -> None:

        super().__init__(
            name="LogsTool",
            description="Retrieves application logs."
        )

        self.telemetry = TelemetryService()

    # -------------------------------------------------------------------------
    # Retrieve Logs
    # -------------------------------------------------------------------------

    async def execute(
        self,
        service_name: str,
        **kwargs,
    ) -> list[Log]:
        """
        Retrieve normalized logs for a service.
        """

        self.log(
            f"Retrieving logs for '{service_name}'."
        )

        logs = await self.telemetry.get_logs(
            service_name=service_name,
            **kwargs,
        )

        self.log(
            f"Retrieved {len(logs)} log(s)."
        )

        return logs

    # -------------------------------------------------------------------------
    # Aggregation
    # -------------------------------------------------------------------------

    async def aggregate(
        self,
        service_name: str,
        **kwargs,
    ):
        """
        Retrieve aggregated log statistics.
        """

        self.log(
            f"Aggregating logs for '{service_name}'."
        )

        return await self.telemetry.aggregate_logs(
            service_name=service_name,
            **kwargs,
        )

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