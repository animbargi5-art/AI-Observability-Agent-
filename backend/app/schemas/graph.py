"""
===============================================================================
TattvaAI - Knowledge Graph Schemas
===============================================================================

This module defines the graph structures used by the TattvaAI AI Reasoning
Engine.

The Knowledge Graph connects:

    • Services
    • Traces
    • Logs
    • Metrics
    • Alerts
    • Dependencies
    • Root Causes

The graph enables explainable reasoning by showing relationships between
different pieces of evidence.

===============================================================================
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import (
    GraphNodeType,
    GraphEdgeType,
)


# =============================================================================
# Graph Node
# =============================================================================

class GraphNode(BaseModel):
    """
    Represents a node inside the Knowledge Graph.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    id: str = Field(
        ...,
        description="Unique node identifier.",
    )

    label: str = Field(
        ...,
        description="Human readable node label.",
    )

    type: GraphNodeType = Field(
        ...,
        description="Node type.",
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


# =============================================================================
# Graph Edge
# =============================================================================

class GraphEdge(BaseModel):
    """
    Relationship between two graph nodes.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    source: str = Field(
        ...,
        description="Source node ID.",
    )

    target: str = Field(
        ...,
        description="Target node ID.",
    )

    relationship: GraphEdgeType = Field(
        ...,
        description="Relationship type.",
    )

    weight: float = Field(
        default=1.0,
        ge=0.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


# =============================================================================
# Knowledge Graph
# =============================================================================

class KnowledgeGraph(BaseModel):
    """
    Complete investigation Knowledge Graph.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    investigation_id: str

    nodes: list[GraphNode] = Field(
        default_factory=list,
    )

    edges: list[GraphEdge] = Field(
        default_factory=list,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )