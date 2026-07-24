from __future__ import annotations

import os
import httpx

from contextlib import AsyncExitStack

from mcp import ClientSession

from mcp.client.streamable_http import (
    streamable_http_client,
)

from app.mcp.config import MCPConfig

class MCPSession:

    def __init__(self):

        self.api_key = MCPConfig.API_KEY

        self.exit_stack = AsyncExitStack()

        self.client = None

        self.read_stream = None

        self.write_stream = None

        self.session = None
    
    async def connect(self):

        if self.session is not None:
            return

        headers = {
            "SIGNOZ-API-KEY": MCPConfig.API_KEY,
        }

        print("=" * 60)
        print("SERVER URL :", MCPConfig.SERVER_URL)
        print("API KEY    :", repr(self.api_key))
        print("HEADERS:", headers)
        print("=" * 60)

        http_client = httpx.AsyncClient(
            headers=headers,
            timeout=httpx.Timeout(
                MCPConfig.TIMEOUT,
                read=300.0,
            ),
        )

        self.client = http_client

        transport = streamable_http_client(
            MCPConfig.SERVER_URL,
            http_client=http_client,
        )

        (
            self.read_stream,
            self.write_stream,
            _,
        ) = await self.exit_stack.enter_async_context(
            transport
        )

        self.session = ClientSession(
            self.read_stream,
            self.write_stream,
        )

        await self.exit_stack.enter_async_context(
            self.session
        )

        await self.session.initialize()

    async def disconnect(self):

        await self.exit_stack.aclose()

        self.client = None
        self.read_stream = None
        self.write_stream = None
        self.session = None

        self.exit_stack = AsyncExitStack()

    async def list_tools(self):

        return await self.session.list_tools()

    async def call_tool(
        self,
        name: str,
        arguments: dict,
    ):

        print("=" * 60)
        print("CALLING TOOL:", name)
        print("SESSION:", self.session)
        print("=" * 60)

        return await self.session.call_tool(
            name=name,
            arguments=arguments,
        )