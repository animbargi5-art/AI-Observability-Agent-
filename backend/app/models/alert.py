"""
===============================================================================
TattvaAI - Alert Domain Model
===============================================================================

Represents a normalized alert used throughout the
TattvaAI investigation pipeline.

This model is transport-independent and represents the canonical
alert object inside TattvaAI.

Every alert retrieved from SigNoz, Prometheus AlertManager, Grafana,
or any external alerting platform must first be converted into this
model before being consumed by the investigation pipeline.

Flow
----
SigNoz / AlertManager / Grafana
        ↓
MCP Gateway
        ↓
Alert Service
        ↓
Alert Tool
        ↓
Alert
        ↓
Alert Agent
        ↓
Evidence

===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Alert(BaseModel):
    """
    Canonical alert model.
    """

    # -------------------------------------------------------------------------
    # Identification
    # -------------------------------------------------------------------------

    alert_id: str

    name: str

    rule_name: Optional[str] = None

    fingerprint: Optional[str] = None

    # -------------------------------------------------------------------------
    # Service Information
    # -------------------------------------------------------------------------

    service_name: str

    service_version: Optional[str] = None

    environment: Optional[str] = None

    namespace: Optional[str] = None

    # -------------------------------------------------------------------------
    # Alert Classification
    # -------------------------------------------------------------------------

    severity: str

    status: str

    source: Optional[str] = None

    # -------------------------------------------------------------------------
    # Alert Description
    # -------------------------------------------------------------------------

    summary: Optional[str] = None

    description: Optional[str] = None

    runbook_url: Optional[str] = None

    # -------------------------------------------------------------------------
    # Ownership
    # -------------------------------------------------------------------------

    owner: Optional[str] = None

    acknowledged: bool = False

    silenced: bool = False

    # -------------------------------------------------------------------------
    # Timing
    # -------------------------------------------------------------------------

    fired_at: Optional[datetime] = None

    resolved_at: Optional[datetime] = None

    last_updated: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Labels / Metadata
    # -------------------------------------------------------------------------

    labels: dict[str, str] = Field(
        default_factory=dict
    )

    annotations: dict[str, str] = Field(
        default_factory=dict
    )

    # -------------------------------------------------------------------------
    # Helper Properties
    # -------------------------------------------------------------------------

    @property
    def active(self) -> bool:
        """
        Returns True if the alert is currently active.
        """

        return self.status.upper() in (
            "FIRING",
            "ACTIVE",
            "OPEN",
        )

    @property
    def resolved(self) -> bool:
        """
        Returns True if the alert has been resolved.
        """

        return self.status.upper() in (
            "RESOLVED",
            "CLOSED",
        )

    @property
    def critical(self) -> bool:
        """
        Returns True for CRITICAL alerts.
        """

        return self.severity.upper() == "CRITICAL"

    @property
    def high(self) -> bool:
        """
        Returns True for HIGH alerts.
        """

        return self.severity.upper() == "HIGH"

    @property
    def medium(self) -> bool:
        """
        Returns True for MEDIUM alerts.
        """

        return self.severity.upper() == "MEDIUM"

    @property
    def low(self) -> bool:
        """
        Returns True for LOW alerts.
        """

        return self.severity.upper() == "LOW"

    @property
    def actionable(self) -> bool:
        """
        Returns True when the alert requires investigation.
        """

        return (
            self.active
            and not self.silenced
        )

    @property
    def requires_attention(self) -> bool:
        """
        Returns True when the alert has not yet been acknowledged.
        """

        return (
            self.active
            and not self.acknowledged
        )

    @property
    def duration_seconds(self) -> Optional[float]:
        """
        Returns the alert duration in seconds.

        If unresolved, the duration is calculated until now.
        """

        if self.fired_at is None:
            return None

        end_time = self.resolved_at or datetime.utcnow()

        return (end_time - self.fired_at).total_seconds()

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def summary_text(self) -> str:
        """
        Returns a concise human-readable summary.
        """

        return (
            f"[{self.severity}] "
            f"{self.service_name} - "
            f"{self.name}"
        )