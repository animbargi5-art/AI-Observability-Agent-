"""
===============================================================================
TattvaAI - Historical Tool
===============================================================================

Purpose
-------
Provides normalized historical incident data for AI investigation agents.

Responsibilities
----------------
• Retrieve historical incidents
• Hide TelemetryService implementation
• Return HistoricalIncident domain models

This tool NEVER:
----------------
❌ Parses JSON
❌ Knows about MCP
❌ Knows about SigNoz response format
❌ Performs AI reasoning

Architecture
------------
HistoricalAgent
        ↓
HistoricalTool
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

from app.core.logger import logger
from app.models.historical_incident import HistoricalIncident
from app.services.telemetry_service import TelemetryService
from app.tools.base_tool import BaseTool


class HistoricalTool(BaseTool):
    """
    Tool responsible for retrieving normalized historical incidents.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Historical Tool",
            description="Retrieves historical incidents from telemetry.",
        )

        self.telemetry = TelemetryService()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    async def execute(
        self,
        service_name: str,
    ) -> list[HistoricalIncident]:
        """
        Retrieve historical incidents for a service.
        """

        logger.info(
            "HistoricalTool: Retrieving historical incidents for '%s'.",
            service_name,
        )

        incidents = await self.telemetry.get_historical_incidents(
            service_name,
        )

        logger.info(
            "HistoricalTool: Retrieved %d historical incident(s).",
            len(incidents),
        )

        return incidents

    async def health_check(self) -> bool:
        """
        Verify telemetry connectivity.
        """

        return await self.telemetry.health_check()