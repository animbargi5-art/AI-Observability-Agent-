"""
===============================================================================
TattvaAI - Tools Package
===============================================================================

This package contains high-level tools used by AI agents.

Each tool is responsible only for collecting and retrieving data.
AI reasoning is performed by the corresponding agent.

Architecture
------------
Agent
    ↓
Tool
    ↓
Service
    ↓
MCP Gateway
    ↓
SigNoz MCP Server

Available Tools
---------------
- TraceTool
- LogsTool
- MetricsTool
- DependencyTool
- HistoricalTool
- AlertTool

===============================================================================
"""

from app.tools.base_tool import BaseTool

from app.tools.trace_tool import TraceTool
from app.tools.logs_tool import LogsTool
from app.tools.metrics_tool import MetricsTool
from app.tools.dependency_tool import DependencyTool
from app.tools.historical_tool import HistoricalTool
from app.tools.alert_tool import AlertTool

__all__ = [

    "BaseTool",

    "TraceTool",

    "LogsTool",

    "MetricsTool",

    "DependencyTool",

    "HistoricalTool",

    "AlertTool",

]