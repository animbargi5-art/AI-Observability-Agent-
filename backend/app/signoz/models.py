"""
===============================================================================
TattvaAI - SigNoz Models
===============================================================================

This module defines the raw telemetry models returned by SigNoz.

These models represent telemetry exactly as received from SigNoz and are
later transformed into the application's internal investigation schemas.

These are NOT Investigation Schemas.

===============================================================================
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# Base Telemetry
# =============================================================================

class TelemetryRecord(BaseModel):
    """
    Base model for all SigNoz telemetry records.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow",
    )

    timestamp: datetime | None = None

    service_name: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# =============================================================================
# Trace
# =============================================================================

class TraceRecord(TelemetryRecord):
    """
    Distributed trace returned by SigNoz.
    """

    trace_id: str

    span_id: str

    parent_span_id: str | None = None

    operation_name: str

    duration_ms: float

    status_code: str

    start_time: datetime | None = None

    end_time: datetime | None = None


# =============================================================================
# Log
# =============================================================================

class LogRecord(TelemetryRecord):
    """
    Log record returned by SigNoz.
    """

    trace_id: str | None = None

    span_id: str | None = None

    level: str

    logger_name: str | None = None

    message: str


# =============================================================================
# Metric
# =============================================================================

class MetricRecord(TelemetryRecord):
    """
    Metric returned by SigNoz.
    """

    metric_name: str

    value: float

    unit: str

    labels: dict[str, Any] = Field(
        default_factory=dict
    )


# =============================================================================
# Alert
# =============================================================================

class AlertRecord(TelemetryRecord):
    """
    Alert returned by SigNoz.
    """

    alert_id: str

    alert_name: str

    severity: str

    state: str

    description: str = ""

    triggered_at: datetime | None = None


# =============================================================================
# Service
# =============================================================================

class ServiceRecord(BaseModel):
    """
    Service discovered inside SigNoz.
    """

    model_config = ConfigDict(extra="allow")

    service_name: str

    environment: str | None = None

    language: str | None = None

    version: str | None = None


# =============================================================================
# Dependency
# =============================================================================

class DependencyRecord(BaseModel):
    """
    Service dependency returned by SigNoz.
    """

    model_config = ConfigDict(extra="allow")

    source_service: str

    target_service: str

    request_count: int = 0

    error_rate: float = 0.0

    latency_ms: float = 0.0


# =============================================================================
# Query Result
# =============================================================================

class QueryResult(BaseModel):
    """
    Generic response returned from SigNoz.
    """

    model_config = ConfigDict(extra="allow")

    success: bool = True

    query: str

    total_records: int = 0

    execution_time_ms: float = 0.0

    data: list[Any] = Field(default_factory=list)