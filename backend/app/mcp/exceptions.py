"""
===============================================================================
TattvaAI - MCP Exceptions
===============================================================================

Generic exceptions used throughout the MCP layer.

This module is provider-independent and may be reused for any MCP server.

Supported Providers
-------------------
- SigNoz
- GitHub
- Kubernetes
- Slack
- Jira
- Future MCP Servers

===============================================================================
"""

from __future__ import annotations

from typing import Any


class MCPException(Exception):
    """
    Base exception for every MCP-related error.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "MCP_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:

        self.message = message

        self.error_code = error_code

        self.details = details or {}

        super().__init__(message)

    def __str__(self) -> str:

        return (
            f"{self.error_code}: {self.message}"
        )


# ============================================================================
# Connection
# ============================================================================

class MCPConnectionError(MCPException):
    """
    Raised when the MCP client cannot connect to a server.
    """

    def __init__(
        self,
        message: str = "Unable to connect to MCP server.",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            error_code="MCP_CONNECTION_ERROR",
            details=details,
        )


class MCPReconnectError(MCPException):
    """
    Raised when automatic reconnection fails.
    """

    def __init__(
        self,
        message: str = "Failed to reconnect to MCP server.",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            error_code="MCP_RECONNECT_ERROR",
            details=details,
        )


# ============================================================================
# Authentication
# ============================================================================

class MCPAuthenticationError(MCPException):
    """
    Raised when authentication fails.
    """

    def __init__(
        self,
        message: str = "Authentication failed.",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            error_code="MCP_AUTHENTICATION_ERROR",
            details=details,
        )


class MCPAuthorizationError(MCPException):
    """
    Raised when authorization is denied.
    """

    def __init__(
        self,
        message: str = "Authorization failed.",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            error_code="MCP_AUTHORIZATION_ERROR",
            details=details,
        )


# ============================================================================
# Tool Execution
# ============================================================================

class MCPToolError(MCPException):
    """
    Raised when an MCP tool execution fails.
    """

    def __init__(
        self,
        tool_name: str,
        message: str = "Tool execution failed.",
        details: dict[str, Any] | None = None,
    ) -> None:

        self.tool_name = tool_name

        super().__init__(
            message=f"{tool_name}: {message}",
            error_code="MCP_TOOL_ERROR",
            details=details,
        )


class MCPToolNotFoundError(MCPException):
    """
    Raised when the requested tool does not exist.
    """

    def __init__(
        self,
        tool_name: str,
    ) -> None:

        super().__init__(
            message=f"Tool '{tool_name}' not found.",
            error_code="MCP_TOOL_NOT_FOUND",
        )


class MCPToolTimeoutError(MCPException):
    """
    Raised when a tool execution exceeds the timeout.
    """

    def __init__(
        self,
        tool_name: str,
    ) -> None:

        super().__init__(
            message=f"Tool '{tool_name}' timed out.",
            error_code="MCP_TOOL_TIMEOUT",
        )


# ============================================================================
# Resources
# ============================================================================

class MCPResourceError(MCPException):
    """
    Raised when a resource cannot be accessed.
    """

    def __init__(
        self,
        resource_uri: str,
        message: str = "Unable to access resource.",
    ) -> None:

        super().__init__(
            message=f"{resource_uri}: {message}",
            error_code="MCP_RESOURCE_ERROR",
        )


# ============================================================================
# Protocol
# ============================================================================

class MCPProtocolError(MCPException):
    """
    Raised when the MCP protocol is violated.
    """

    def __init__(
        self,
        message: str = "Protocol error.",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            error_code="MCP_PROTOCOL_ERROR",
            details=details,
        )


class MCPTransportError(MCPException):
    """
    Raised when the transport layer fails.
    """

    def __init__(
        self,
        message: str = "Transport failure.",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            error_code="MCP_TRANSPORT_ERROR",
            details=details,
        )


# ============================================================================
# Server
# ============================================================================

class MCPServerError(MCPException):
    """
    Raised when the remote MCP server reports an error.
    """

    def __init__(
        self,
        message: str = "Remote MCP server returned an error.",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            error_code="MCP_SERVER_ERROR",
            details=details,
        )


# ============================================================================
# Validation
# ============================================================================

class MCPValidationError(MCPException):
    """
    Raised when request validation fails.
    """

    def __init__(
        self,
        message: str = "Validation failed.",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            error_code="MCP_VALIDATION_ERROR",
            details=details,
        )


# ============================================================================
# Configuration
# ============================================================================

class MCPConfigurationError(MCPException):
    """
    Raised when the MCP client configuration is invalid.
    """

    def __init__(
        self,
        message: str = "Invalid MCP configuration.",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            error_code="MCP_CONFIGURATION_ERROR",
            details=details,
        )