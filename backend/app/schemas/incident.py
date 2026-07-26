"""
===============================================================================
TattvaAI - Incident Schema
===============================================================================

This module defines the Incident schema.

An Incident is the starting point of every investigation inside TattvaAI.

Incidents may originate from:

    • SigNoz Alerts
    • Manual User Trigger
    • AI Agent Detection
    • Scheduled Health Checks
    • External Monitoring Systems

The Incident object contains only metadata describing the incident.

It DOES NOT contain:

    • Evidence
    • Root Cause
    • Recommendations
    • Timeline
    • Knowledge Graph

Those are represented by their own schemas.

===============================================================================
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import (
    InvestigationStatus,
    Severity,
)


class Incident(BaseModel):
    """
    Represents a production incident.

    This object is created when an alert or anomaly is detected
    and serves as the entry point for the AI investigation workflow.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    incident_id: str = Field(
        ...,
        description="Unique identifier for the incident.",
    )

    title: str = Field(
        ...,
        description="Short incident title.",
    )

    description: str = Field(
        default="",
        description="Detailed description of the incident.",
    )

    # -------------------------------------------------------------------------
    # Service Information
    # -------------------------------------------------------------------------

    service_name: str = Field(
        ...,
        description="Primary affected service.",
    )

    environment: str = Field(
        default="production",
        description="Deployment environment.",
    )

    source: str = Field(
        default="SigNoz",
        description="Origin of the incident.",
    )

    # -------------------------------------------------------------------------
    # Severity & Status
    # -------------------------------------------------------------------------

    severity: Severity = Field(
        default=Severity.MEDIUM,
        description="Incident severity.",
    )

    status: InvestigationStatus = Field(
        default=InvestigationStatus.PENDING,
        description="Current investigation status.",
    )

    # -------------------------------------------------------------------------
    # Correlation
    # -------------------------------------------------------------------------

    trace_id: str | None = Field(
        default=None,
        description="Associated Trace ID.",
    )

    span_id: str | None = Field(
        default=None,
        description="Associated Span ID.",
    )

    alert_id: str | None = Field(
        default=None,
        description="Associated Alert ID.",
    )

    # -------------------------------------------------------------------------
    # Time Information
    # -------------------------------------------------------------------------

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Incident creation timestamp.",
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp.",
    )

    # -------------------------------------------------------------------------
    # Additional Metadata
    # -------------------------------------------------------------------------

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional incident metadata.",
    )