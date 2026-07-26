"""
===============================================================================
TattvaAI - Timeline Schemas
===============================================================================

This module defines the timeline models used during an investigation.

The timeline provides a chronological record of every important event that
occurs during the investigation lifecycle.

Examples:
    • Incident Created
    • Trace Agent Started
    • Logs Collected
    • Metrics Correlated
    • Knowledge Graph Built
    • Root Cause Identified
    • Recommendations Generated
    • Investigation Completed

===============================================================================
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import (
    AgentType,
    InvestigationStage,
    TimelineEventType,
)


# =============================================================================
# Timeline Event
# =============================================================================

class TimelineEvent(BaseModel):
    """
    Represents a single event in the investigation timeline.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    id: str = Field(
        ...,
        description="Unique timeline event identifier.",
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Time when the event occurred.",
    )

    event_type: TimelineEventType = Field(
        ...,
        description="Type of timeline event.",
    )

    stage: InvestigationStage = Field(
        ...,
        description="Investigation stage during this event.",
    )

    agent: AgentType | None = Field(
        default=None,
        description="Agent responsible for the event.",
    )

    title: str = Field(
        ...,
        description="Short event title.",
    )

    description: str = Field(
        default="",
        description="Detailed event description.",
    )

    success: bool = Field(
        default=True,
        description="Whether the event completed successfully.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional event metadata.",
    )


# =============================================================================
# Investigation Timeline
# =============================================================================

class InvestigationTimeline(BaseModel):
    """
    Complete investigation timeline.

    Stores all timeline events in chronological order.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    investigation_id: str = Field(
        ...,
        description="Associated investigation ID.",
    )

    events: list[TimelineEvent] = Field(
        default_factory=list,
        description="Chronological investigation events.",
    )

    started_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Investigation start time.",
    )

    completed_at: datetime | None = Field(
        default=None,
        description="Investigation completion time.",
    )

    duration_seconds: float | None = Field(
        default=None,
        description="Total investigation duration.",
    )