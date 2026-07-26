"""
===============================================================================
TattvaAI - Graph Builder
===============================================================================

Purpose
-------
Builds and compiles the LangGraph investigation workflow.

Responsibilities
----------------
• Build workflow
• Compile workflow
• Expose compiled graph

This module is the single entry point used by the IncidentCoordinator.

Flow
----
Workflow
    ↓
Compile
    ↓
Executable Graph

===============================================================================
"""

from __future__ import annotations

from langgraph.graph.state import CompiledStateGraph

from app.graph.workflow import build_workflow


class GraphBuilder:
    """
    Builds and compiles the TattvaAI investigation graph.
    """

    def __init__(self) -> None:

        self.workflow = build_workflow()

    # -------------------------------------------------------------------------
    # Compile
    # -------------------------------------------------------------------------

    def compile(self) -> CompiledStateGraph:
        """
        Compile the LangGraph workflow.
        """

        return self.workflow.compile()


# =============================================================================
# Global Graph Instance
# =============================================================================

graph: CompiledStateGraph = GraphBuilder().compile()