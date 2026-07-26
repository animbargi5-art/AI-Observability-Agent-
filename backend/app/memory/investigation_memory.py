"""
===============================================================================
TattvaAI - Investigation Memory
===============================================================================

This module implements the shared Investigation Memory used by all AI agents.

The InvestigationMemory acts as the single source of truth during an
investigation. Every AI agent reads from and writes to this memory.

Responsibilities
----------------
• Store the InvestigationState
• Manage collected evidence
• Manage investigation timeline
• Store Knowledge Graph
• Store Root Cause
• Store Recommendations
• Store Investigation Summary

This module DOES NOT contain:

• AI logic
• SigNoz logic
• Database logic
• API logic

===============================================================================
"""

from datetime import datetime

from app.schemas import (
    Incident,
    InvestigationState,
    InvestigationSummary,
    Evidence,
    CorrelatedEvidence,
    InvestigationTimeline,
    TimelineEvent,
    KnowledgeGraph,
    RootCause,
    RootCauseHypothesis,
    Recommendation,
)

from app.core.enums import (
    InvestigationStage,
    InvestigationStatus,
)


class InvestigationMemory:
    """
    Shared memory used during an investigation.

    Every AI agent receives the same InvestigationMemory instance,
    allowing agents to collaborate by reading and updating the same
    InvestigationState.
    """

    def __init__(self, state: InvestigationState):

        self._state = state

    # =======================================================================
    # State
    # =======================================================================

    def get_state(self) -> InvestigationState:
        """
        Return the complete investigation state.
        """

        return self._state

    # =======================================================================
    # Incident
    # =======================================================================

    def set_incident(self, incident: Incident) -> None:
        """
        Store incident information.
        """

        self._state.incident = incident
        self._touch()

    # =======================================================================
    # Status
    # =======================================================================

    def set_status(self, status: InvestigationStatus) -> None:
        """
        Update investigation status.
        """

        self._state.status = status
        self._touch()

    def set_stage(self, stage: InvestigationStage) -> None:
        """
        Update current investigation stage.
        """

        self._state.stage = stage
        self._touch()

    # =======================================================================
    # Evidence
    # =======================================================================

    def add_evidence(self, evidence: Evidence) -> None:
        """
        Add one evidence item.
        """

        self._state.evidence.append(evidence)
        self._touch()

    def add_correlated_evidence(
        self,
        evidence: CorrelatedEvidence,
    ) -> None:
        """
        Store correlated evidence.
        """

        self._state.correlated_evidence.append(evidence)
        self._touch()

    # =======================================================================
    # Timeline
    # =======================================================================

    def set_timeline(
        self,
        timeline: InvestigationTimeline,
    ) -> None:
        """
        Replace the complete investigation timeline.
        """

        self._state.timeline = timeline
        self._touch()

    def add_timeline_event(
        self,
        event: TimelineEvent,
    ) -> None:
        """
        Append one event to the timeline.
        """

        if self._state.timeline is None:

            self._state.timeline = InvestigationTimeline(
                investigation_id=self._state.investigation_id
            )

        self._state.timeline.events.append(event)

        self._touch()

    # =======================================================================
    # Knowledge Graph
    # =======================================================================

    def set_graph(
        self,
        graph: KnowledgeGraph,
    ) -> None:
        """
        Store the generated Knowledge Graph.
        """

        self._state.graph = graph

        self._touch()

    # =======================================================================
    # AI Reasoning
    # =======================================================================

    def add_hypothesis(
        self,
        hypothesis: RootCauseHypothesis,
    ) -> None:
        """
        Store one root cause hypothesis.
        """

        self._state.hypotheses.append(hypothesis)

        self._touch()

    def set_root_cause(
        self,
        root_cause: RootCause,
    ) -> None:
        """
        Store the final root cause.
        """

        self._state.root_cause = root_cause

        self._touch()

    def set_confidence(
        self,
        confidence: float,
    ) -> None:
        """
        Update overall investigation confidence.
        """

        self._state.confidence_score = confidence

        self._touch()

    # =======================================================================
    # Recommendations
    # =======================================================================

    def add_recommendation(
        self,
        recommendation: Recommendation,
    ) -> None:
        """
        Add one recommendation.
        """

        self._state.recommendations.append(recommendation)

        self._touch()

    # =======================================================================
    # Summary
    # =======================================================================

    def set_summary(
        self,
        summary: InvestigationSummary,
    ) -> None:
        """
        Store final investigation summary.
        """

        self._state.summary = summary

        self._touch()

    # =======================================================================
    # Utility
    # =======================================================================

    def clear(self) -> None:
        """
        Reset investigation memory.

        Keeps the same investigation but clears generated data.
        """

        self._state.evidence.clear()

        self._state.correlated_evidence.clear()

        self._state.hypotheses.clear()

        self._state.recommendations.clear()

        self._state.timeline = None

        self._state.graph = None

        self._state.root_cause = None

        self._state.summary = None

        self._state.confidence_score = 0.0

        self._state.stage = InvestigationStage.INITIALIZED

        self._state.status = InvestigationStatus.PENDING

        self._touch()

    # =======================================================================
    # Internal Helpers
    # =======================================================================

    def _touch(self) -> None:
        """
        Update the last modified timestamp.
        """

        self._state.updated_at = datetime.utcnow()