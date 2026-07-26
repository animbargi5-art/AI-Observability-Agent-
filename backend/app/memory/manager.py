"""
===============================================================================
TattvaAI - Investigation Memory Manager
===============================================================================

Manages the active investigation state shared across the entire AI
investigation workflow.

Responsibilities
----------------
• Create a new investigation
• Store the current InvestigationState
• Return the active investigation
• Replace/update the investigation state
• Reset the investigation

This class is intentionally lightweight. All investigation data is stored
inside InvestigationState.

Flow
----
API
    ↓
Coordinator
    ↓
InvestigationMemory
    ↓
InvestigationState
    ↓
LangGraph Agents

===============================================================================
"""

from __future__ import annotations

from typing import Optional

from app.schemas.investigation_state import InvestigationState


class InvestigationMemory:
    """
    Stores the current investigation state.

    Only one investigation is active per InvestigationMemory instance.
    """

    def __init__(self) -> None:
        self._state: Optional[InvestigationState] = None

    # -------------------------------------------------------------------------
    # Create
    # -------------------------------------------------------------------------

    def create(
        self,
        incident_id: str,
        service_name: str,
    ) -> InvestigationState:
        """
        Create a new investigation state.
        """

        self._state = InvestigationState(
            incident_id=incident_id,
            service_name=service_name,
        )

        return self._state

    # -------------------------------------------------------------------------
    # Read
    # -------------------------------------------------------------------------

    def get(self) -> InvestigationState:
        """
        Return the active investigation state.
        """

        if self._state is None:
            raise RuntimeError(
                "No active investigation exists."
            )

        return self._state

    def has_active_investigation(self) -> bool:
        """
        Check whether an investigation is active.
        """

        return self._state is not None

    # -------------------------------------------------------------------------
    # Update
    # -------------------------------------------------------------------------

    def update(
        self,
        state: InvestigationState,
    ) -> InvestigationState:
        """
        Replace the current investigation state.
        """

        self._state = state

        return self._state

    # -------------------------------------------------------------------------
    # Reset
    # -------------------------------------------------------------------------

    def clear(self) -> None:
        """
        Remove the current investigation.
        """

        self._state = None

    # -------------------------------------------------------------------------
    # Convenience
    # -------------------------------------------------------------------------

    def incident_id(self) -> str | None:
        """
        Return the active incident ID.
        """

        if self._state is None:
            return None

        return self._state.incident_id

    def service_name(self) -> str | None:
        """
        Return the active service name.
        """

        if self._state is None:
            return None

        return self._state.service_name