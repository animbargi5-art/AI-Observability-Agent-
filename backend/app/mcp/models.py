"""
===============================================================================
TattvaAI - Generic MCP Models
===============================================================================

This module defines generic data models used by the Model Context Protocol (MCP)
layer.

These models are provider-agnostic and can represent tools, resources,
prompts, server metadata, and tool execution results from any MCP server.

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

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ============================================================================
# Server Information
# ============================================================================

class MCPServerInfo(BaseModel):
    """
    Information about a connected MCP server.
    """

    name: str

    version: str

    protocol_version: str

    description: str | None = None

    capabilities: dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# Tool Metadata
# ============================================================================

class MCPTool(BaseModel):
    """
    Represents one MCP tool.
    """

    name: str

    description: str

    input_schema: dict[str, Any] = Field(default_factory=dict)

    annotations: dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# Tool Call Request
# ============================================================================

class MCPToolCall(BaseModel):
    """
    Represents one tool execution request.
    """

    tool_name: str

    arguments: dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# Tool Result
# ============================================================================

class MCPToolResult(BaseModel):
    """
    Result returned by an MCP tool.
    """

    success: bool = True

    tool_name: str

    structured_content: Any | None = None

    content: list[Any] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    error: str | None = None

    execution_time_ms: float | None = None


# ============================================================================
# Resource Metadata
# ============================================================================

class MCPResource(BaseModel):
    """
    Represents one MCP resource.
    """

    uri: str

    name: str

    description: str | None = None

    mime_type: str | None = None


# ============================================================================
# Resource Content
# ============================================================================

class MCPResourceContent(BaseModel):
    """
    Content returned by an MCP resource.
    """

    uri: str

    content: Any

    metadata: dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# Prompt Metadata
# ============================================================================

class MCPPrompt(BaseModel):
    """
    Represents one MCP prompt.
    """

    name: str

    description: str | None = None

    arguments: list[dict[str, Any]] = Field(default_factory=list)


# ============================================================================
# Connection Information
# ============================================================================

class MCPConnectionInfo(BaseModel):
    """
    Current MCP connection state.
    """

    connected: bool = False

    server_url: str | None = None

    transport: str | None = None

    connected_at: datetime | None = None

    last_activity: datetime | None = None


# ============================================================================
# Health Status
# ============================================================================

class MCPHealthStatus(BaseModel):
    """
    Health status of the MCP client.
    """

    healthy: bool = True

    message: str = "OK"

    checked_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Tool Execution Statistics
# ============================================================================

class MCPExecutionStats(BaseModel):
    """
    Statistics for MCP tool execution.
    """

    total_calls: int = 0

    successful_calls: int = 0

    failed_calls: int = 0

    average_latency_ms: float = 0.0