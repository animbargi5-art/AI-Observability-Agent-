"""
===============================================================================
TattvaAI - Investigation Engine
===============================================================================

Purpose
-------
Coordinates the complete AI reasoning pipeline.

This engine DOES NOT:
---------------------
❌ Query SigNoz
❌ Retrieve telemetry
❌ Parse JSON

It ONLY orchestrates the reasoning engines.

Flow
----
InvestigationState
        ↓
CorrelationEngine
        ↓
RootCauseEngine
        ↓
RecommendationEngine
        ↓
ReasoningEngine
        ↓
Updated InvestigationState

===============================================================================
"""

from __future__ import annotations

from app.decision.correlation_engine import CorrelationEngine
from app.decision.reasoning_engine import ReasoningEngine
from app.decision.recommendation_engine import RecommendationEngine
from app.decision.root_cause_engine import RootCauseEngine

from app.schemas.investigation_state import InvestigationState


class InvestigationEngine:
    """
    Main AI reasoning pipeline.
    """

    def __init__(self):

        self.correlation_engine = CorrelationEngine()

        self.root_cause_engine = RootCauseEngine()

        self.recommendation_engine = RecommendationEngine()

        self.reasoning_engine = ReasoningEngine()

    # ------------------------------------------------------------------
    # Execute Investigation
    # ------------------------------------------------------------------

    def execute(
        self,
        state: InvestigationState,
    ) -> InvestigationState:

        # --------------------------------------------------------------
        # Correlation Phase
        # --------------------------------------------------------------

        state = self.correlation_engine.execute(
            state
        )

        # --------------------------------------------------------------
        # Root Cause Phase
        # --------------------------------------------------------------

        state = self.root_cause_engine.execute(
            state
        )

        # --------------------------------------------------------------
        # Recommendation Phase
        # --------------------------------------------------------------

        state = self.recommendation_engine.execute(
            state
        )

        # --------------------------------------------------------------
        # Investigation Summary
        # --------------------------------------------------------------

        reasoning = self.reasoning_engine.execute(
            state
        )

        #
        # Store reasoning summary.
        #
        # If InvestigationState does not yet contain a
        # `reasoning` field, add one:
        #
        # reasoning: dict[str, Any] = Field(default_factory=dict)
        #

        state.reasoning = reasoning

        state.timeline.append(
            "Investigation Engine completed AI reasoning."
        )

        return state