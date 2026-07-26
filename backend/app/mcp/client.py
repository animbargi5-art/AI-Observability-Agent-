from __future__ import annotations

import os
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from app.core.logger import logger
from app.core.settings import settings

from app.mcp.session import mcp_session

from app.mcp.exceptions import (
    MCPConnectionError,
    MCPToolError,
    MCPToolTimeoutError,
)


class MCPClient:
    """
    Official MCP SDK client.

    Responsible only for:

    • Opening the HTTP transport
    • Creating ClientSession
    • Initializing the MCP protocol
    • Executing tools
    • Closing the connection

    Provider-independent.
    """

    def __init__(self):

        self.server_url = settings.SIGNOZ_MCP_SERVER

        self.api_key = settings.SIGNOZ_API_KEY

        self.exit_stack = AsyncExitStack()

        self.transport = None

        self.read_stream = None

        self.write_stream = None

        self.session: ClientSession | None = None

    # -------------------------------------------------------------------------
    # Connection
    # -------------------------------------------------------------------------

    async def connect(self) -> None:

        if self.session is not None:
            return

        logger.info(
            "Connecting to MCP server: %s",
            self.server_url,
        )

        try:

            headers = {}

            if self.api_key:

                headers["SIGNOZ-API-KEY"] = self.api_key

            self.transport = streamablehttp_client(
                self.server_url,
                headers=headers,
            )

            (
                self.read_stream,
                self.write_stream,
                _,
            ) = await self.exit_stack.enter_async_context(
                self.transport
            )

            self.session = ClientSession(
                self.read_stream,
                self.write_stream,
            )

            await self.exit_stack.enter_async_context(
                self.session
            )

            await self.session.initialize()

            await mcp_session.connect(
                self,
                self.server_url,
            )

            await mcp_session.mark_initialized()

            logger.info(
                "Headers being sent: %s",headers
            )

        except Exception as ex:

            raise MCPConnectionError(
                str(ex)
            ) from ex

    
    # -------------------------------------------------------------------------
    # Disconnect
    # -------------------------------------------------------------------------

    async def disconnect(self) -> None:

        if self.session is None:
            return

        logger.info("Closing MCP connection...")

        try:

            await self.exit_stack.aclose()

        finally:

            self.session = None

            self.transport = None

            self.read_stream = None

            self.write_stream = None

            await mcp_session.disconnect()

            logger.info("MCP connection closed.")

    # -------------------------------------------------------------------------
    # Execute Tool
    # -------------------------------------------------------------------------

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict | None = None,
    ):

        if self.session is None:

            raise MCPConnectionError(
                "MCP client is not connected."
            )

        arguments = arguments or {}

        logger.info(
            "Calling MCP Tool: %s",
            tool_name,
        )

        try:

            result = await self.session.call_tool(
                tool_name,
                arguments,
            )

            await mcp_session.heartbeat()

            return result

        except TimeoutError as ex:

            raise MCPToolTimeoutError(
                tool_name
            ) from ex

        except Exception as ex:

            raise MCPToolError(
                tool_name=tool_name,
                message=str(ex),
            ) from ex

    # -------------------------------------------------------------------------
    # List Tools
    # -------------------------------------------------------------------------

    async def list_tools(self):

        if self.session is None:

            raise MCPConnectionError(
                "MCP client is not connected."
            )

        tools = await self.session.list_tools()

        await mcp_session.heartbeat()

        return tools

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    @property
    def connected(self) -> bool:

        return self.session is not None

    # -------------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------------

    async def health_check(self) -> bool:

        return self.connected