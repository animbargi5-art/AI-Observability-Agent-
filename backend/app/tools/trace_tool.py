"""
===============================================================================
TattvaAI - Trace Tool
===============================================================================

Purpose
-------
Provides normalized distributed trace data for AI investigation agents.

Responsibilities
----------------
• Retrieve traces
• Hide TelemetryService implementation
• Return normalized Trace models

This tool NEVER:
----------------
❌ Performs AI reasoning
❌ Parses raw MCP responses
❌ Knows about LangGraph

===============================================================================
"""

from __future__ import annotations

from app.core.logger import logger

from app.models.trace import Trace
from app.services.telemetry_service import TelemetryService
from app.tools.base_tool import BaseTool


class TraceTool(BaseTool):
    """
    Tool responsible for retrieving distributed traces.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Trace Tool",
            description="Retrieves distributed traces.",
        )

        self.telemetry = TelemetryService()


    # -------------------------------------------------------------------------
    # Execute
    # -------------------------------------------------------------------------

    async def execute(
        self,
        service_name: str,
        **kwargs,
    ) -> list[Trace]:
        """
        Retrieve normalized traces.
        """

        logger.info(
            "TraceTool: Retrieving traces for '%s'.",
            service_name,
        )

        traces = await self.telemetry.get_traces(
            service_name=service_name,
            **kwargs,
        )

        logger.info(
            "TraceTool: Retrieved %d traces.",
            len(traces),
        )

        return traces

    # -------------------------------------------------------------------------
    # Aggregate
    # -------------------------------------------------------------------------

    async def aggregate(
        self,
        service_name: str,
        **kwargs,
    ):
        """
        Retrieve aggregated trace information.
        """

        logger.info(
            "TraceTool: Aggregating traces for '%s'.",
            service_name,
        )

        return await self.telemetry.aggregate_traces(
            service_name=service_name,
            **kwargs,
        )

    # -------------------------------------------------------------------------
    # Trace Details
    # -------------------------------------------------------------------------

    async def trace_details(
        self,
        trace_id: str,
    ):
        """
        Retrieve a single trace by ID.
        """

        logger.info(
            "TraceTool: Retrieving trace '%s'.",
            trace_id,
        )

        return await self.telemetry.get_trace_details(
            trace_id=trace_id,
        )

    # -------------------------------------------------------------------------
    # Health Check
    # -------------------------------------------------------------------------

    async def health_check(self) -> bool:
        """
        Verify telemetry connectivity.
        """

        return await self.telemetry.health_check()