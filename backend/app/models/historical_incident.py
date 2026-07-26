"""
===============================================================================
TattvaAI - Historical Incident Domain Model
===============================================================================

Represents a previously resolved investigation retrieved from historical
storage.

Historical incidents are used by the AI Investigation Engine to identify
recurring failures, improve confidence, and recommend proven solutions.

This model is transport-independent and represents the canonical
historical incident object inside TattvaAI.

Flow
----
Database / SigNoz / Knowledge Base
        ↓
Historical Tool
        ↓
Historical Incident
        ↓
Historical Agent
        ↓
Evidence
        ↓
Correlation Engine

===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class HistoricalIncident(BaseModel):
    """
    Canonical historical investigation.
    """

    # -------------------------------------------------------------------------
    # Identification
    # -------------------------------------------------------------------------

    incident_id: str

    title: str

    # -------------------------------------------------------------------------
    # Service Information
    # -------------------------------------------------------------------------

    service_name: str

    endpoint: Optional[str] = None

    operation: Optional[str] = None

    environment: Optional[str] = None

    # -------------------------------------------------------------------------
    # Incident Classification
    # -------------------------------------------------------------------------

    severity: str

    status: str

    # -------------------------------------------------------------------------
    # Investigation Results
    # -------------------------------------------------------------------------

    root_cause: str

    resolution: str

    confidence: int = Field(
        ge=0,
        le=100,
    )

    # -------------------------------------------------------------------------
    # Similarity
    # -------------------------------------------------------------------------

    similarity_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    occurrence_count: int = 1

    # -------------------------------------------------------------------------
    # Previous Investigation Metadata
    # -------------------------------------------------------------------------

    resolved_by: Optional[str] = None

    previous_recommendation: Optional[str] = None

    # -------------------------------------------------------------------------
    # Timing
    # -------------------------------------------------------------------------

    started_at: Optional[datetime] = None

    resolved_at: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    tags: list[str] = Field(
        default_factory=list
    )

    metadata: dict[str, str] = Field(
        default_factory=dict
    )

    # -------------------------------------------------------------------------
    # Helper Properties
    # -------------------------------------------------------------------------

    @property
    def recurring(self) -> bool:
        """
        Returns True if this incident has occurred multiple times.
        """

        return self.occurrence_count > 1

    @property
    def highly_similar(self) -> bool:
        """
        Returns True if this incident is highly similar to the
        current investigation.
        """

        return self.similarity_score >= 0.80

    @property
    def recently_resolved(self) -> bool:
        """
        Returns True if the incident was resolved within the last 30 days.
        """

        if self.resolved_at is None:
            return False

        return (
            datetime.utcnow() - self.resolved_at
        ).days <= 30

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def summary_text(self) -> str:
        """
        Returns a concise human-readable summary.
        """

        return (
            f"{self.service_name} | "
            f"{self.root_cause} | "
            f"{self.similarity_score:.2f} similarity"
        )