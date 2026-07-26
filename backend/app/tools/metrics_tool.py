"""
===============================================================================
TattvaAI - Metrics Tool
===============================================================================

Purpose
-------
Provides normalized metric data for AI investigation agents.

Responsibilities
----------------
• Retrieve normalized metrics
• Hide TelemetryService implementation
• Return Metric domain models

This tool NEVER:
----------------
❌ Parses JSON
❌ Knows about MCP
❌ Knows about SigNoz response format
❌ Performs AI reasoning

Architecture
------------
MetricsAgent
        ↓
MetricsTool
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

from app.models.metric import Metric

from app.services.telemetry_service import TelemetryService

from app.tools.base_tool import BaseTool


class MetricsTool(BaseTool):
    """
    Tool responsible for retrieving normalized metrics.
    """

    def __init__(self):

        super().__init__(
            name="Metrics Tool",
            description="Retrieves application metrics.",
        )
        
        self.telemetry = TelemetryService()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    async def execute(
        self,
        service_name: str,
        metric_name: str,
        **kwargs,
    ) -> list[Metric]:
        """
        Retrieve normalized metrics.
        """

        logger.info(
            "MetricsTool: Retrieving '%s' metrics for '%s'",
            metric_name,
            service_name,
        )

        metrics = await self.telemetry.get_metrics(
            service_name=service_name,
            metric_name=metric_name,
            **kwargs,
        )

        logger.info(
            "MetricsTool: Retrieved %d metric records.",
            len(metrics),
        )

        return metrics

    async def list_metrics(self):
        """
        List all available metrics.
        """

        logger.info(
            "MetricsTool: Listing available metrics."
        )

        return await self.telemetry.signoz.list_metrics()

    async def top_metrics(self):
        """
        Retrieve top metrics.
        """

        logger.info(
            "MetricsTool: Retrieving top metrics."
        )

        return await self.telemetry.signoz.top_metrics()

    async def health_check(self) -> bool:
        """
        Verify telemetry connectivity.
        """

        return await self.telemetry.health_check()