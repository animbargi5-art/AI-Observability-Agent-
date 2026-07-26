"""
===============================================================================
TattvaAI - LangGraph Workflow
===============================================================================

Purpose
-------
Defines the investigation workflow executed by LangGraph.

This module is responsible ONLY for defining:

• Workflow nodes
• Workflow edges

It does NOT:

❌ Execute investigations
❌ Perform AI reasoning
❌ Query SigNoz

Flow
----
START
    ↓
Trace
    ↓
Logs
    ↓
Metrics
    ↓
Dependency
    ↓
Historical
    ↓
Alert
    ↓
Investigation
    ↓
Report
    ↓
END

===============================================================================
"""

from __future__ import annotations

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.graph.state import InvestigationState

from app.graph.nodes import (
    trace_node,
    logs_node,
    metrics_node,
    dependency_node,
    historical_node,
    alert_node,
    investigation_node,
    report_node,
)


def build_workflow() -> StateGraph:
    """
    Build the LangGraph workflow.

    Returns
    -------
    StateGraph
        Configured investigation workflow.
    """

    workflow = StateGraph(
        InvestigationState
    )

    # ------------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------------

    workflow.add_node(
        "trace",
        trace_node,
    )

    workflow.add_node(
        "logs",
        logs_node,
    )

    workflow.add_node(
        "metrics",
        metrics_node,
    )

    workflow.add_node(
        "dependency",
        dependency_node,
    )

    workflow.add_node(
        "historical",
        historical_node,
    )

    workflow.add_node(
        "alert",
        alert_node,
    )

    workflow.add_node(
        "investigation",
        investigation_node,
    )

    workflow.add_node(
        "report",
        report_node,
    )

    # ------------------------------------------------------------------
    # Workflow
    # ------------------------------------------------------------------

    workflow.add_edge(
        START,
        "trace",
    )

    workflow.add_edge(
        "trace",
        "logs",
    )

    workflow.add_edge(
        "logs",
        "metrics",
    )

    workflow.add_edge(
        "metrics",
        "dependency",
    )

    workflow.add_edge(
        "dependency",
        "historical",
    )

    workflow.add_edge(
        "historical",
        "alert",
    )

    workflow.add_edge(
        "alert",
        "investigation",
    )

    workflow.add_edge(
        "investigation",
        "report",
    )

    workflow.add_edge(
        "report",
        END,
    )

    return workflow