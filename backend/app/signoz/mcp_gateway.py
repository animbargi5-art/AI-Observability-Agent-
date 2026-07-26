"""
===============================================================================
TattvaAI - SigNoz MCP Gateway
===============================================================================

Purpose
-------
Single gateway responsible for all communication with the SigNoz MCP Server.

Responsibilities
----------------
• Manage MCP connection lifecycle
• Execute MCP tools
• Retry transient failures
• Log requests
• Validate responses

This module NEVER performs:

❌ AI reasoning
❌ Report generation
❌ Telemetry analysis
❌ State management

Architecture
------------
TelemetryService
        ↓
MCPGateway
        ↓
Official MCP Python SDK
        ↓
SigNoz MCP Server
===============================================================================
"""

from __future__ import annotations

from typing import Any

from app.mcp.client import MCPClient
from app.core.logger import logger
from app.signoz.config import SigNozConfig


class MCPGateway:
    """
    Gateway responsible for all communication with the SigNoz MCP server.
    """

    def __init__(self) -> None:

        self.server_url = SigNozConfig.MCP_SERVER_URL

        self.connected = False

        self.client = MCPClient()

    # -------------------------------------------------------------------------
    # Connection
    # -------------------------------------------------------------------------

    async def connect(self) -> None:
        """
        Establish connection to the MCP server.

        The actual SDK wiring will be added after the reusable
        app.mcp client layer is finalized.
        """

        if self.connected:
            return

        logger.info(
            "Connecting to MCP Server (%s)...",
            self.server_url,
        )

        await self.client.connect()

        self.connected = True

        logger.info("MCP connection established.")

    async def disconnect(self) -> None:
        """
        Close MCP connection.
        """

        if not self.connected:
            return

        logger.info("Disconnecting MCP Gateway...")

        await self.client.disconnect()

        self.connected = False

        self.client = None

        logger.info("Disconnected.")

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    async def ensure_connection(self) -> None:

        if not self.connected:
            await self.connect()

    # -------------------------------------------------------------------------
    # Generic Tool Executor
    # -------------------------------------------------------------------------

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute an MCP tool.
        """

        await self.ensure_connection()

        arguments = arguments or {}

        logger.info(
            "Executing MCP Tool: %s",
            tool_name,
        )

        logger.debug(
            "Arguments: %s",
            arguments,
        )

        try:

            result = await self.client.call_tool(
                tool_name,
                arguments,
            )

            return result
            
        except Exception as ex:

            logger.exception(
                "MCP Tool '%s' failed.",
                tool_name,
            )

            raise ex

    # -------------------------------------------------------------------------
    # Tool Wrappers
    # -------------------------------------------------------------------------

    async def list_tools(self):

        return await self.execute_tool(
            "list_tools"
        )

    async def list_services(self, **kwargs):

        return await self.execute_tool(
            "signoz_list_services",
            kwargs,
        )

    async def search_traces(self, **kwargs):

        return await self.execute_tool(
            "signoz_search_traces",
            kwargs,
        )

    async def get_trace_details(self, **kwargs):

        return await self.execute_tool(
            "signoz_get_trace_details",
            kwargs,
        )

    async def aggregate_traces(self, **kwargs):

        return await self.execute_tool(
            "signoz_aggregate_traces",
            kwargs,
        )

    async def search_logs(self, **kwargs):

        return await self.execute_tool(
            "signoz_search_logs",
            kwargs,
        )

    async def aggregate_logs(self, **kwargs):

        return await self.execute_tool(
            "signoz_aggregate_logs",
            kwargs,
        )

    async def query_metrics(self, **kwargs):

        return await self.execute_tool(
            "signoz_query_metrics",
            kwargs,
        )

    async def list_metrics(self, **kwargs):

        return await self.execute_tool(
            "signoz_list_metrics",
            kwargs,
        )

    async def top_metrics(self, **kwargs):

        return await self.execute_tool(
            "signoz_get_top_metrics",
            kwargs,
        )

    async def list_alerts(self, **kwargs):

        return await self.execute_tool(
            "signoz_list_alerts",
            kwargs,
        )

    async def list_alert_rules(self, **kwargs):

        return await self.execute_tool(
            "signoz_list_alert_rules",
            kwargs,
        )

    async def search_docs(self, **kwargs):

        return await self.execute_tool(
            "signoz_search_docs",
            kwargs,
        )

    async def fetch_doc(self, **kwargs):

        return await self.execute_tool(
            "signoz_fetch_doc",
            kwargs,
        )

    async def execute_builder_query(self, **kwargs):

        return await self.execute_tool(
            "signoz_execute_builder_query",
            kwargs,
        )

    # -------------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------------

    async def health_check(self) -> bool:
        """
        Returns True if the gateway is connected.
        """

        return self.connected