"""
===============================================================================
TattvaAI - SigNoz Integration Package
===============================================================================

This package provides all SigNoz-related functionality used by TattvaAI.

Modules
-------
config.py
    SigNoz configuration and environment settings.

models.py
    Pydantic models representing SigNoz telemetry.

query_builder.py
    Builds standardized telemetry queries.

mcp_gateway.py
    Generic gateway for communicating with the SigNoz MCP Server.

telemetry_service.py
    High-level telemetry access service.

alert_service.py
    Alert management service.

documentation_service.py
    Official SigNoz documentation service.

===============================================================================
"""

from app.signoz.config import SigNozConfig
from app.signoz.models import (
    TraceRecord,
    LogRecord,
    MetricRecord,
    ServiceRecord,
    AlertRecord,
)

from app.signoz.query_builder import QueryBuilder
from app.signoz.mcp_gateway import MCPGateway

from app.signoz.telemetry_service import TelemetryService
from app.signoz.alert_service import AlertService
from app.signoz.documentation_service import DocumentationService

__all__ = [
    "SigNozConfig",

    "TraceRecord",
    "LogRecord",
    "MetricRecord",
    "ServiceRecord",
    "AlertRecord",

    "QueryBuilder",

    "MCPGateway",

    "TelemetryService",

    "AlertService",

    "DocumentationService",
]