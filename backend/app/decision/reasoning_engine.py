"""
===============================================================================
TattvaAI - Reasoning Engine
===============================================================================

Purpose
-------
Summarizes the investigation results produced by the AI reasoning pipeline.

Responsibilities
----------------
• Analyze correlated evidence
• Summarize root causes
• Summarize recommendations
• Produce investigation statistics

Flow
----
Correlation
        ↓
RootCause
        ↓
Recommendation
        ↓
Reasoning Summary
===============================================================================
"""

from __future__ import annotations

from app.schemas.investigation_state import InvestigationState


class ReasoningEngine:
    """
    Produces a high-level reasoning summary from the investigation state.
    """

    def execute(
        self,
        state: InvestigationState,
    ) -> dict:

        services = sorted(
            {
                correlation.service_name
                for correlation in state.correlations
            }
        )

        highest_severity = self.highest_severity(state)

        highest_confidence = self.highest_confidence(state)

        return {

            "services": services,

            "highest_severity": highest_severity,

            "confidence": highest_confidence,

            "evidence_count": len(state.evidence),

            "correlation_count": len(state.correlations),

            "root_cause_count": len(state.root_causes),

            "recommendation_count": len(state.recommendations),

            "timeline_events": len(state.timeline),

            "summary": self.build_summary(
                state,
                services,
                highest_severity,
            ),
        }

    # -------------------------------------------------------------------------
    # Highest Severity
    # -------------------------------------------------------------------------

    def highest_severity(
        self,
        state: InvestigationState,
    ) -> str:

        priority = {

            "CRITICAL": 4,

            "HIGH": 3,

            "MEDIUM": 2,

            "LOW": 1,

        }

        highest = "LOW"

        for root in state.root_causes:

            if priority.get(root.severity, 0) > priority.get(highest, 0):

                highest = root.severity

        return highest

    # -------------------------------------------------------------------------
    # Highest Confidence
    # -------------------------------------------------------------------------

    def highest_confidence(
        self,
        state: InvestigationState,
    ) -> int:

        if not state.root_causes:

            return 0

        return max(

            root.confidence

            for root in state.root_causes

        )

    # -------------------------------------------------------------------------
    # Summary Builder
    # -------------------------------------------------------------------------

    def build_summary(
        self,
        state: InvestigationState,
        services: list[str],
        severity: str,
    ) -> str:

        service_text = ", ".join(services)

        if not service_text:

            service_text = "None"

        return (

            f"Investigation completed. "

            f"{len(state.evidence)} evidence item(s), "

            f"{len(state.correlations)} correlation(s), "

            f"{len(state.root_causes)} root cause(s), "

            f"{len(state.recommendations)} recommendation(s). "

            f"Highest severity: {severity}. "

            f"Affected services: {service_text}."

        )