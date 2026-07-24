from __future__ import annotations

import os

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from contextlib import AsyncExitStack

from app.mcp.exceptions import (
    MCPConnectionError,
    MCPResponseError,
    MCPTimeoutError,
)

class MCPClient:

    def __init__(self):

        self.server_url = os.getenv(
            "SIGNOZ_MCP_SERVER",
            "http://localhost:8001/mcp",
        )

        self.api_key = os.getenv("SIGNOZ_SERVICE_ACCOUNT_KEY")

        self.session = None

        self.read_stream = None
        self.write_stream = None
        self.transport = None
        self.exit_stack = AsyncExitStack()

    async def connect(self):
        headers = {
            "SIGNOZ-API-KEY": self.api_key,
        }

        transport = streamablehttp_client(
            self.server_url,
            headers=headers,
        )

        self.transport = transport