"""
===============================================================================
TattvaAI - Trace Domain Model
===============================================================================

Represents a normalized distributed trace used throughout the
TattvaAI investigation pipeline.

This model is transport-independent and is the canonical representation
of a distributed trace inside TattvaAI.

Every trace retrieved from SigNoz, OpenTelemetry, or any external
observability platform must first be converted into this model before
being consumed by the investigation pipeline.

Flow
----
SigNoz / OpenTelemetry
        ↓
MCP Gateway
        ↓
Telemetry Service
        ↓
Trace Tool
        ↓
Trace
        ↓
Trace Agent
        ↓
Evidence

===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Trace(BaseModel):
    """
    Canonical distributed trace model.
    """

    # -------------------------------------------------------------------------
    # Identification
    # -------------------------------------------------------------------------

    trace_id: str

    span_id: Optional[str] = None

    parent_span_id: Optional[str] = None

    # -------------------------------------------------------------------------
    # Service Information
    # -------------------------------------------------------------------------

    service_name: str

    service_version: Optional[str] = None

    operation_name: str

    endpoint: Optional[str] = None

    http_method: Optional[str] = None

    span_kind: Optional[str] = None

    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------

    duration_ms: float = 0.0

    status_code: Optional[int] = None

    status: str = "UNKNOWN"

    error_message: Optional[str] = None

    # -------------------------------------------------------------------------
    # Infrastructure
    # -------------------------------------------------------------------------

    host: Optional[str] = None

    environment: Optional[str] = None

    namespace: Optional[str] = None

    # -------------------------------------------------------------------------
    # OpenTelemetry Resource Attributes
    # -------------------------------------------------------------------------

    resource_attributes: dict[str, str] = Field(
        default_factory=dict
    )

    attributes: dict[str, str] = Field(
        default_factory=dict
    )

    # -------------------------------------------------------------------------
    # Timing
    # -------------------------------------------------------------------------

    timestamp: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Helper Properties
    # -------------------------------------------------------------------------

    @property
    def successful(self) -> bool:
        """
        Returns True when the request completed successfully.
        """

        return (
            self.status_code is not None
            and 200 <= self.status_code < 400
        )

    @property
    def failed(self) -> bool:
        """
        Returns True for server failures.
        """

        return (
            self.status_code is not None
            and self.status_code >= 500
        )

    @property
    def client_error(self) -> bool:
        """
        Returns True for HTTP 4xx responses.
        """

        return (
            self.status_code is not None
            and 400 <= self.status_code < 500
        )

    @property
    def slow(self) -> bool:
        """
        Indicates critical latency.
        """

        return self.duration_ms >= 1000

    @property
    def warning(self) -> bool:
        """
        Indicates moderate latency.
        """

        return 500 <= self.duration_ms < 1000

    @property
    def healthy(self) -> bool:
        """
        Indicates healthy latency.
        """

        return self.duration_ms < 200

    @property
    def has_error(self) -> bool:
        """
        Returns True if an explicit error message exists.
        """

        return bool(self.error_message)

    @property
    def root_span(self) -> bool:
        """
        Returns True when this span is the root span of the trace.
        """

        return self.parent_span_id is None

    @property
    def latency_category(self) -> str:
        """
        Returns a human-readable latency category.
        """

        if self.duration_ms < 200:
            return "HEALTHY"

        if self.duration_ms < 500:
            return "NORMAL"

        if self.duration_ms < 1000:
            return "WARNING"

        return "CRITICAL"

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def exceeds_latency(
        self,
        threshold_ms: float,
    ) -> bool:
        """
        Returns True if the trace exceeds the supplied latency threshold.
        """

        return self.duration_ms >= threshold_ms

    def summary(self) -> str:
        """
        Returns a concise human-readable description of the trace.
        """

        endpoint = self.endpoint or self.operation_name

        return (
            f"{self.service_name} | "
            f"{endpoint} | "
            f"{self.duration_ms:.2f} ms | "
            f"HTTP {self.status_code}"
        )