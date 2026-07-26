"""
===============================================================================
TattvaAI - MCP Tool Executor
===============================================================================

This module provides a generic interface for executing tools exposed by any
Model Context Protocol (MCP) server.

Responsibilities
----------------
• Execute MCP tools
• Validate tool names
• Retry failed executions
• Handle errors
• Record execution statistics

This module is provider-independent.

===============================================================================
"""

from __future__ import annotations

import asyncio
from time import perf_counter
from typing import Any

from app.core.logger import logger

from app.mcp.config import mcp_config
from app.mcp.exceptions import (
    MCPConnectionError,
    MCPToolError,
    MCPToolTimeoutError,
)
from app.mcp.models import MCPToolCall, MCPToolResult


class MCPToolExecutor:
    """
    Generic MCP tool execution layer.
    """

    def __init__(self, client) -> None:

        self.client = client

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ) -> MCPToolResult:
        """
        Execute one MCP tool.
        """

        arguments = arguments or {}

        request = MCPToolCall(
            tool_name=tool_name,
            arguments=arguments,
        )

        return await self._execute_with_retry(request)

    # ---------------------------------------------------------------------
    # Retry Logic
    # ---------------------------------------------------------------------

    async def _execute_with_retry(
        self,
        request: MCPToolCall,
    ) -> MCPToolResult:

        last_error: Exception | None = None

        for attempt in range(
            1,
            mcp_config.MAX_RETRIES + 1,
        ):

            try:

                return await self._execute_once(request)

            except MCPToolTimeoutError as exc:

                last_error = exc

                logger.warning(
                    f"Timeout executing '{request.tool_name}' "
                    f"(attempt {attempt}/{mcp_config.MAX_RETRIES})"
                )

            except MCPConnectionError as exc:

                last_error = exc

                logger.warning(
                    f"Connection failed while executing "
                    f"'{request.tool_name}' "
                    f"(attempt {attempt}/{mcp_config.MAX_RETRIES})"
                )

            except MCPToolError:

                raise

            await asyncio.sleep(
                mcp_config.RETRY_BACKOFF_SECONDS
            )

        raise MCPToolError(
            tool_name=request.tool_name,
            message="Maximum retry attempts exceeded.",
            details={
                "last_error": str(last_error)
            },
        )

    # ---------------------------------------------------------------------
    # Single Execution
    # ---------------------------------------------------------------------

    async def _execute_once(
        self,
        request: MCPToolCall,
    ) -> MCPToolResult:

        logger.info(
            f"Executing MCP tool: {request.tool_name}"
        )

        started = perf_counter()

        #
        # NOTE
        #
        # MCPClient.call_tool(...)
        #
        # will be implemented in client.py
        #

        response = await self.client.call_tool(
            request.tool_name,
            request.arguments,
        )

        elapsed = (
            perf_counter() - started
        ) * 1000

        return MCPToolResult(

            success=True,

            tool_name=request.tool_name,

            structured_content=response,

            execution_time_ms=elapsed,

        )