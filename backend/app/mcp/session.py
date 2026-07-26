"""
===============================================================================
TattvaAI - MCP Session Manager
===============================================================================

Maintains the lifecycle and state of MCP client connections.

Responsibilities
----------------
• Connection state
• Session lifecycle
• Health status
• Connection timestamps
• Async synchronization

This module is provider-independent.

===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Optional

from app.core.logger import logger


class MCPSession:
    """
    Stores the lifecycle state of one MCP connection.
    """

    def __init__(self) -> None:

        self.connected: bool = False

        self.initialized: bool = False

        self.server_url: Optional[str] = None

        self.connected_at: Optional[datetime] = None

        self.last_activity: Optional[datetime] = None

        self.client = None

        self.lock = asyncio.Lock()

    # -------------------------------------------------------------------------
    # Connection State
    # -------------------------------------------------------------------------

    async def connect(
        self,
        client,
        server_url: str,
    ) -> None:
        """
        Register a connected MCP client.
        """

        async with self.lock:

            self.client = client

            self.server_url = server_url

            self.connected = True

            self.connected_at = datetime.utcnow()

            self.last_activity = datetime.utcnow()

            logger.info(
                "MCP session connected."
            )

    async def disconnect(self) -> None:
        """
        Clear the current session.
        """

        async with self.lock:

            self.client = None

            self.connected = False

            self.initialized = False

            self.connected_at = None

            self.last_activity = None

            logger.info(
                "MCP session disconnected."
            )

    async def mark_initialized(self) -> None:
        """
        Mark the MCP protocol as initialized.
        """

        async with self.lock:

            self.initialized = True

            self.last_activity = datetime.utcnow()

    async def heartbeat(self) -> None:
        """
        Update last activity timestamp.
        """

        async with self.lock:

            self.last_activity = datetime.utcnow()

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    def is_connected(self) -> bool:

        return self.connected

    def is_initialized(self) -> bool:

        return self.initialized

    def get_client(self):

        return self.client

    def get_server_url(self) -> Optional[str]:

        return self.server_url

    def get_connected_at(self) -> Optional[datetime]:

        return self.connected_at

    def get_last_activity(self) -> Optional[datetime]:

        return self.last_activity

    # -------------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------------

    def health(self) -> dict:
        """
        Return current session health.
        """

        return {

            "connected": self.connected,

            "initialized": self.initialized,

            "server_url": self.server_url,

            "connected_at": self.connected_at,

            "last_activity": self.last_activity,

        }


#
# Singleton session
#

mcp_session = MCPSession()