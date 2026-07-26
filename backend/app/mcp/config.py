"""
===============================================================================
TattvaAI - MCP Configuration
===============================================================================

This module contains the global configuration for all Model Context Protocol
(MCP) connections used throughout TattvaAI.

It is intentionally generic and does NOT contain any SigNoz-specific logic.

Responsibilities
----------------
• MCP transport configuration
• Client timeouts
• Retry policy
• Authentication defaults
• Protocol version
• Connection limits

Used By
-------
- MCP Client
- MCP Session Manager
- MCP Gateway
- Future MCP Providers (GitHub, Kubernetes, Slack, etc.)

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class MCPConfig:
    """
    Global configuration for MCP connections.
    """

    # -------------------------------------------------------------------------
    # Protocol
    # -------------------------------------------------------------------------

    PROTOCOL_NAME: Final[str] = "Model Context Protocol"

    PROTOCOL_VERSION: Final[str] = "2026-07-28"

    CLIENT_NAME: Final[str] = "TattvaAI"

    CLIENT_VERSION: Final[str] = "1.0.0"

    # -------------------------------------------------------------------------
    # Transport
    # -------------------------------------------------------------------------

    DEFAULT_TRANSPORT: Final[str] = "streamable_http"

    VERIFY_SSL: Final[bool] = False

    # -------------------------------------------------------------------------
    # Connection
    # -------------------------------------------------------------------------

    CONNECTION_TIMEOUT: Final[int] = 30

    READ_TIMEOUT: Final[int] = 60

    WRITE_TIMEOUT: Final[int] = 30

    KEEP_ALIVE_TIMEOUT: Final[int] = 30

    # -------------------------------------------------------------------------
    # Retry Policy
    # -------------------------------------------------------------------------

    MAX_RETRIES: Final[int] = 3

    RETRY_BACKOFF_SECONDS: Final[int] = 2

    RETRY_ON_TIMEOUT: Final[bool] = True

    # -------------------------------------------------------------------------
    # Health Checks
    # -------------------------------------------------------------------------

    ENABLE_HEALTH_CHECK: Final[bool] = True

    HEALTH_CHECK_INTERVAL: Final[int] = 60

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------

    ENABLE_REQUEST_LOGGING: Final[bool] = True

    ENABLE_RESPONSE_LOGGING: Final[bool] = False

    ENABLE_DEBUG_LOGGING: Final[bool] = False

    # -------------------------------------------------------------------------
    # Resources
    # -------------------------------------------------------------------------

    ENABLE_RESOURCE_CACHE: Final[bool] = True

    RESOURCE_CACHE_TTL: Final[int] = 300

    # -------------------------------------------------------------------------
    # Tool Execution
    # -------------------------------------------------------------------------

    TOOL_EXECUTION_TIMEOUT: Final[int] = 120

    MAX_CONCURRENT_TOOL_CALLS: Final[int] = 10

    # -------------------------------------------------------------------------
    # Session
    # -------------------------------------------------------------------------

    AUTO_RECONNECT: Final[bool] = True

    RECONNECT_DELAY_SECONDS: Final[int] = 5

    MAX_RECONNECT_ATTEMPTS: Final[int] = 5


mcp_config = MCPConfig()