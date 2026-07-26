"""
===============================================================================
TattvaAI - SigNoz Telemetry Service
===============================================================================

Purpose
-------
Provides a high-level interface for retrieving telemetry data from SigNoz.

Responsibilities
----------------
• Search traces
• Retrieve trace details
• Search logs
• Query metrics
• Retrieve dependencies
• Retrieve services
• Execute Query Builder requests

This service hides the MCP Gateway from the application layer.

Architecture
------------
Application Service
        ↓
SigNoz Telemetry Service
        ↓
Query Builder
        ↓
MCP Gateway
        ↓
SigNoz MCP Server
===============================================================================
"""

from __future__ import annotations

from typing import Any

from app.core.logger import logger
from app.signoz.mcp_gateway import MCPGateway
from app.signoz.query_builder import QueryBuilder


class TelemetryService:
    """
    SigNoz telemetry interface.
    """

    def __init__(self) -> None:

        self.gateway = MCPGateway()

        self.query_builder = QueryBuilder()

    # =====================================================================
    # Internal Executor
    # =====================================================================

    async def _execute(
        self,
        tool_name: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute one MCP tool.
        """

        payload = payload or {}

        logger.info(
            "TelemetryService -> %s",
            tool_name,
        )

        return await self.gateway.execute_tool(
            tool_name,
            payload,
        )

    # =====================================================================
    # Traces
    # =====================================================================

    async def search_traces(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_trace_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_search_traces",
            payload,
        )

    async def get_trace_details(
        self,
        trace_id: str,
    ) -> Any:

        return await self._execute(
            "signoz_get_trace_details",
            {
                "trace_id": trace_id,
            },
        )

    async def aggregate_traces(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_trace_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_aggregate_traces",
            payload,
        )

    # =====================================================================
    # Logs
    # =====================================================================

    async def search_logs(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_log_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_search_logs",
            payload,
        )

    async def aggregate_logs(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_log_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_aggregate_logs",
            payload,
        )

    # =====================================================================
    # Metrics
    # =====================================================================

    async def query_metrics(
        self,
        service_name: str,
        metric_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_metric_query(
            service_name=service_name,
            metric_name=metric_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_query_metrics",
            payload,
        )

    async def list_metrics(self) -> Any:

        return await self._execute(
            "signoz_list_metrics",
        )

    async def top_metrics(self) -> Any:

        return await self._execute(
            "signoz_get_top_metrics",
        )

    # =====================================================================
    # Services
    # =====================================================================

    async def list_services(self) -> Any:

        return await self._execute(
            "signoz_list_services",
        )

    async def get_service_top_operations(
        self,
        service_name: str,
    ) -> Any:

        return await self._execute(
            "signoz_get_service_top_operations",
            {
                "service_name": service_name,
            },
        )

    # =====================================================================
    # Dependencies
    # =====================================================================

    async def get_dependencies(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_dependency_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_execute_builder_query",
            payload,
        )

    # =====================================================================
    # Historical Traces
    # =====================================================================

    async def get_historical_traces(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:
        """
        Historical traces currently reuse the standard trace search.
        Later this can be extended with explicit time-range filters.
        """

        payload = self.query_builder.build_trace_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_search_traces",
            payload,
        )

    # =====================================================================
    # Generic Query Builder
    # =====================================================================

    async def execute_builder_query(
        self,
        payload: dict[str, Any],
    ) -> Any:

        return await self._execute(
            "signoz_execute_builder_query",
            payload,
        )

    # =====================================================================
    # Health
    # =====================================================================

    async def health_check(self) -> bool:
        """
        Check whether the gateway is connected.
        """

        return await self.gateway.health_check()