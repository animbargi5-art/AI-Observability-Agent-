"""
===============================================================================
TattvaAI - Root Cause Engine
===============================================================================

Determines the most probable root cause of an incident using correlated
investigation evidence.

Flow
----
Correlation
        ↓
Root Cause Engine
        ↓
RootCause
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from app.models.root_cause import RootCause
from app.models.correlation import Correlation
from app.schemas.investigation_state import InvestigationState


class RootCauseEngine:
    """
    Determines the most probable root cause from correlated evidence.
    """

    SEVERITY_PRIORITY = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }

    def execute(
        self,
        state: InvestigationState,
    ) -> InvestigationState:

        if not state.correlations:

            state.timeline.append(
                "Root Cause Engine: No correlations found."
            )

            return state

        ranked = sorted(

            state.correlations,

            key=lambda c: (
                self.SEVERITY_PRIORITY.get(
                    c.severity,
                    0,
                ),
                c.confidence,
            ),

            reverse=True,

        )

        root_causes = []

        highest = ranked[0]

        root_causes.append(

            self.build_root_cause(
                highest
            )

        )

        state.root_causes = root_causes

        state.timeline.append(
            f"Root Cause Engine identified "
            f"{len(root_causes)} probable root cause(s)."
        )

        return state

    # -----------------------------------------------------------------
    # Build Root Cause
    # -----------------------------------------------------------------

    def build_root_cause(
        self,
        correlation: Correlation,
    ) -> RootCause:

        probable = self.determine_cause(
            correlation
        )

        reasoning = self.build_reasoning(
            correlation
        )

        endpoints = []

        for evidence in correlation.evidence:

            if evidence.endpoint:

                endpoints.append(
                    evidence.endpoint
                )

        endpoints = sorted(
            list(set(endpoints))
        )

        return RootCause(

            service_name=correlation.service_name,

            severity=correlation.severity,

            confidence=correlation.confidence,

            title="Most Probable Root Cause",

            summary=correlation.summary,

            probable_cause=probable,

            reasoning=reasoning,

            correlations=[correlation],

            impacted_services=correlation.impacted_services,

            affected_endpoints=endpoints,

            evidence_count=correlation.evidence_count,

            correlation_count=1,

            priority=self.priority(
                correlation.severity
            ),

            cause_type="Application",

            detected_at=datetime.utcnow(),

        )

    # -----------------------------------------------------------------
    # AI Decision Logic
    # -----------------------------------------------------------------

    def determine_cause(
        self,
        correlation: Correlation,
    ) -> str:

        causes = correlation.possible_causes

        if causes:

            return causes[0]

        return (
            "Unable to determine a definitive root cause."
        )

    # -----------------------------------------------------------------
    # AI Reasoning
    # -----------------------------------------------------------------

    def build_reasoning(
        self,
        correlation: Correlation,
    ) -> list[str]:

        reasoning = [

            f"Service '{correlation.service_name}' "
            f"contains {correlation.evidence_count} "
            f"correlated evidence item(s).",

            f"Highest observed severity: "
            f"{correlation.severity}.",

            f"Correlation confidence: "
            f"{correlation.confidence}%."

        ]

        for cause in correlation.possible_causes:

            reasoning.append(
                f"Observed indicator: {cause}"
            )

        return reasoning

    # -----------------------------------------------------------------
    # Priority
    # -----------------------------------------------------------------

    def priority(
        self,
        severity: str,
    ) -> str:

        mapping = {

            "CRITICAL": "P1",

            "HIGH": "P2",

            "MEDIUM": "P3",

            "LOW": "P4",

        }

        return mapping.get(
            severity,
            "P4",
        )
