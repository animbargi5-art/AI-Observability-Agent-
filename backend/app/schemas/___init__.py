"""
===============================================================================
TattvaAI - Schemas Package
===============================================================================

This package contains all Pydantic schemas used throughout the
TattvaAI Autonomous Incident Investigation Platform.

The schemas define the shared data models exchanged between:

    • API Layer
    • AI Agents
    • Investigation Memory
    • LangGraph Workflow
    • Database
    • Report Generator
    • Frontend

===============================================================================
"""

# =============================================================================
# Incident
# =============================================================================

from .incident import Incident

# =============================================================================
# Timeline
# =============================================================================

from .timeline import (
    TimelineEvent,
    InvestigationTimeline,
)

# =============================================================================
# Knowledge Graph
# =============================================================================

from .graph import (
    GraphNode,
    GraphEdge,
    KnowledgeGraph,
)

# =============================================================================
# Investigation
# =============================================================================

from .investigation import (
    InvestigationState,
    InvestigationSummary,
)

# =============================================================================
# Public Exports
# =============================================================================

__all__ = [
    # Incident
    "Incident",

    # Evidence
    "Evidence",
    "TraceEvidence",
    "LogEvidence",
    "MetricEvidence",
    "DependencyEvidence",
    "HistoricalEvidence",
    "AlertEvidence",
    "CorrelatedEvidence",

    # Timeline
    "TimelineEvent",
    "InvestigationTimeline",

    # Root Cause
    "RootCause",
    "RootCauseHypothesis",

    # Recommendation
    "Recommendation",
    "RecommendationAction",
    "RecommendationSummary",

    # Knowledge Graph
    "GraphNode",
    "GraphEdge",
    "KnowledgeGraph",

    # Investigation
    "InvestigationState",
    "InvestigationSummary",
]