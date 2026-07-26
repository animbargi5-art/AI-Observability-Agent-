"""
===============================================================================
TattvaAI - Incident Coordinator
===============================================================================

Purpose
-------
Entry point for every AI investigation.

Responsibilities
----------------
• Create InvestigationState
• Start the LangGraph workflow
• Return the completed InvestigationState

This class does NOT:
--------------------
❌ Query SigNoz
❌ Analyze telemetry
❌ Perform AI reasoning
❌ Generate reports

Flow
----
API
    ↓
IncidentCoordinator
    ↓
InvestigationState
    ↓
LangGraph Workflow
    ↓
Completed InvestigationState

===============================================================================
"""

from __future__ import annotations

from uuid import uuid4
from app.schemas.investigation_state import InvestigationState
from app.graph.graph_builder import graph


class IncidentCoordinator:
    """
    Starts a complete AI investigation.
    """

    def __init__(self) -> None:
        pass

    # -------------------------------------------------------------------------
    # Start Investigation
    # -------------------------------------------------------------------------

    async def start_investigation(
        self,
        service_name: str,
        incident_id: str | None = None,
    ) -> InvestigationState:

        if incident_id is None:
            incident_id = f"INC-{uuid4().hex[:8].upper()}"

        # -------------------------------------------------------------
        # Create initial investigation state
        # -------------------------------------------------------------

        state = InvestigationState(

            incident_id=incident_id,

            service_name=service_name,

        )

        # -------------------------------------------------------------
        # Execute LangGraph Workflow
        # -------------------------------------------------------------

        result = await graph.ainvoke(state)

        return result

    # -------------------------------------------------------------------------
    # Alias
    # -------------------------------------------------------------------------

    def run(
        self,
        incident_id: str,
        service_name: str,
    ) -> InvestigationState:

        return self.start_investigation(

            incident_id,

            service_name,

        )