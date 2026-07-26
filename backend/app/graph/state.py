"""
===============================================================================
TattvaAI - Graph State
===============================================================================

Purpose
-------
Provides the shared state used throughout the LangGraph workflow.

The graph layer does NOT define its own state model.

Instead, it reuses the canonical InvestigationState defined under
app.schemas.investigation_state.

This ensures every agent, engine, and graph node operates on the same
state object.

Architecture
------------
FastAPI
    ↓
IncidentCoordinator
    ↓
LangGraph
    ↓
InvestigationState
    ↓
Agents
    ↓
Decision Engines
    ↓
Report Agent

===============================================================================
"""

from __future__ import annotations

from app.schemas.investigation_state import InvestigationState

__all__ = [
    "InvestigationState",
]