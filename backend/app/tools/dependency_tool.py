"""
===============================================================================
TattvaAI - Dependency Tool
===============================================================================

Purpose
-------
Provides normalized service dependency data for AI investigation agents.

Responsibilities
----------------
• Retrieve normalized service dependencies
• Hide TelemetryService implementation
• Return Dependency domain models

This tool NEVER:
----------------
❌ Parses JSON
❌ Knows about MCP
❌ Knows about SigNoz response format
❌ Performs AI reasoning

Architecture
------------
DependencyAgent
        ↓
DependencyTool
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

from app.models.dependency import Dependency

from app.services.telemetry_service import TelemetryService

from app.tools.base_tool import BaseTool


class DependencyTool(BaseTool):
    """
    Tool responsible for retrieving normalized service dependencies.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Dependency Tool",
            description="Retrieves service dependency topology from SigNoz.",
        )

        self.telemetry = TelemetryService()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    async def execute(
        self,
        service_name: str,
        **kwargs,
    ) -> list[Dependency]:
        """
        Retrieve normalized service dependencies.
        """

        logger.info(
            "DependencyTool: Retrieving dependencies for '%s'",
            service_name,
        )

        dependencies = await self.telemetry.get_dependencies(
            service_name=service_name,
            **kwargs,
        )

        logger.info(
            "DependencyTool: Retrieved %d dependencies.",
            len(dependencies),
        )

        return dependencies

    async def health_check(self) -> bool:
        """
        Verify telemetry connectivity.
        """

        return await self.telemetry.health_check()