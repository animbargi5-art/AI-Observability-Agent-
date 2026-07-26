"""
===============================================================================
TattvaAI - Dependency Domain Model
===============================================================================

Represents a normalized service dependency used throughout the
TattvaAI investigation pipeline.

This model is transport-independent and represents the canonical
service dependency inside TattvaAI.

Every dependency retrieved from SigNoz, OpenTelemetry, Jaeger, or any
other observability platform must first be converted into this model
before being consumed by the investigation pipeline.

Flow
----
SigNoz / OpenTelemetry
        ↓
MCP Gateway
        ↓
Telemetry Service
        ↓
Dependency Tool
        ↓
Dependency
        ↓
Dependency Agent
        ↓
Evidence

===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Dependency(BaseModel):
    """
    Canonical service dependency.
    """

    # -------------------------------------------------------------------------
    # Identification
    # -------------------------------------------------------------------------

    dependency_id: Optional[str] = None

    # -------------------------------------------------------------------------
    # Service Relationship
    # -------------------------------------------------------------------------

    source_service: str

    target_service: str

    relationship: str = "calls"

    # -------------------------------------------------------------------------
    # Traffic Statistics
    # -------------------------------------------------------------------------

    request_count: int = 0

    success_count: int = 0

    error_count: int = 0

    error_rate: float = 0.0

    # -------------------------------------------------------------------------
    # Latency Statistics
    # -------------------------------------------------------------------------

    average_latency_ms: float = 0.0

    p50_latency_ms: float = 0.0

    p95_latency_ms: float = 0.0

    p99_latency_ms: float = 0.0

    # -------------------------------------------------------------------------
    # Environment
    # -------------------------------------------------------------------------

    environment: Optional[str] = None

    namespace: Optional[str] = None

    protocol: Optional[str] = None

    service_version: Optional[str] = None

    # -------------------------------------------------------------------------
    # Failure Information
    # -------------------------------------------------------------------------

    failure_reason: Optional[str] = None

    # -------------------------------------------------------------------------
    # Time
    # -------------------------------------------------------------------------

    timestamp: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Additional Metadata
    # -------------------------------------------------------------------------

    attributes: dict[str, str] = Field(
        default_factory=dict
    )

    # -------------------------------------------------------------------------
    # Helper Properties
    # -------------------------------------------------------------------------

    @property
    def healthy(self) -> bool:
        """
        Returns True if the dependency is healthy.
        """

        return (
            self.error_rate < 1
            and self.average_latency_ms < 500
        )

    @property
    def degraded(self) -> bool:
        """
        Returns True when the dependency shows degraded performance.
        """

        return (
            1 <= self.error_rate < 5
            or 500 <= self.average_latency_ms < 1000
        )

    @property
    def critical(self) -> bool:
        """
        Returns True when the dependency is in a critical state.
        """

        return (
            self.error_rate >= 5
            or self.p99_latency_ms >= 2000
        )

    @property
    def availability(self) -> float:
        """
        Returns the availability percentage.
        """

        if self.request_count == 0:
            return 100.0

        return (
            (self.success_count / self.request_count)
            * 100
        )

    @property
    def has_errors(self) -> bool:
        """
        Returns True if errors were observed.
        """

        return self.error_count > 0

    @property
    def is_internal(self) -> bool:
        """
        Returns True if both services belong to the same namespace.
        """

        return (
            self.namespace is not None
            and self.namespace != ""
        )

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def exceeds_latency(
        self,
        threshold_ms: float,
    ) -> bool:
        """
        Returns True if average latency exceeds the supplied threshold.
        """

        return self.average_latency_ms >= threshold_ms

    def summary(self) -> str:
        """
        Returns a concise human-readable summary.
        """

        return (
            f"{self.source_service} -> "
            f"{self.target_service} | "
            f"{self.average_latency_ms:.2f} ms | "
            f"{self.error_rate:.2f}% errors"
        )