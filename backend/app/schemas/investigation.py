"""
===============================================================================
TattvaAI - Investigation Schema
===============================================================================

This module defines the shared InvestigationState used throughout the
TattvaAI Autonomous Incident Investigation Platform.

The InvestigationState is the central object shared between:

    • Incident Coordinator
    • AI Agents
    • Investigation Memory
    • LangGraph Workflow
    • Knowledge Graph Builder
    • Root Cause Engine
    • Recommendation Engine
    • Report Generator
    • Frontend Dashboard

It represents the current state of an investigation.

===============================================================================
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import (
    AgentType,
    InvestigationStage,
    InvestigationStatus,
)

from app.schemas.incident import Incident
from app.schemas.evidence import (
    Evidence,
    CorrelatedEvidence,
)
from app.schemas.timeline import InvestigationTimeline
from app.schemas.root_cause import (
    RootCause,
    RootCauseHypothesis,
)
from app.schemas.recommendation import Recommendation
from app.schemas.graph import KnowledgeGraph


# =============================================================================
# Investigation Summary
# =============================================================================

class InvestigationSummary(BaseModel):
    """
    Final investigation summary.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    overview: str = ""

    conclusion: str = ""

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


# =============================================================================
# Investigation State
# =============================================================================

class InvestigationState(BaseModel):
    """
    Shared investigation state used by all AI agents.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    # -------------------------------------------------------------------------
    # Investigation Information
    # -------------------------------------------------------------------------

    investigation_id: str

    incident: Incident

    status: InvestigationStatus = InvestigationStatus.PENDING

    stage: InvestigationStage = InvestigationStage.INITIALIZED

    current_agent: AgentType | None = None

    started_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    completed_at: datetime | None = None

    # -------------------------------------------------------------------------
    # Shared Investigation Memory
    # -------------------------------------------------------------------------

    memory: Any = None

    # -------------------------------------------------------------------------
    # Evidence
    # -------------------------------------------------------------------------

    evidence: list[Evidence] = Field(
        default_factory=list,
    )

    correlated_evidence: list[CorrelatedEvidence] = Field(
        default_factory=list,
    )

    # -------------------------------------------------------------------------
    # Timeline
    # -------------------------------------------------------------------------

    timeline: InvestigationTimeline | None = None

    # -------------------------------------------------------------------------
    # Knowledge Graph
    # -------------------------------------------------------------------------

    graph: KnowledgeGraph | None = None

    # -------------------------------------------------------------------------
    # AI Reasoning
    # -------------------------------------------------------------------------

    hypotheses: list[RootCauseHypothesis] = Field(
        default_factory=list,
    )

    root_cause: RootCause | None = None

    confidence_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    # -------------------------------------------------------------------------
    # Recommendations
    # -------------------------------------------------------------------------

    recommendations: list[Recommendation] = Field(
        default_factory=list,
    )

    # -------------------------------------------------------------------------
    # Final Summary
    # -------------------------------------------------------------------------

    summary: InvestigationSummary | None = None

    # -------------------------------------------------------------------------
    # Additional Metadata
    # -------------------------------------------------------------------------

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )