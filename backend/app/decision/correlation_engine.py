"""
===============================================================================
TattvaAI - Correlation Engine
===============================================================================

Purpose
-------
Correlates investigation evidence collected by AI agents.

Responsibilities
----------------
• Read Evidence objects
• Group evidence by service
• Calculate severity
• Calculate confidence
• Build Correlation objects
• Store correlations in InvestigationState

Flow
----
Evidence
    ↓
Correlation Engine
    ↓
Correlation
    ↓
Root Cause Agent

===============================================================================
"""

from __future__ import annotations

from collections import defaultdict

from app.models.correlation import Correlation
from app.models.evidence import Evidence
from app.schemas.investigation_state import InvestigationState


class CorrelationEngine:
    """
    Correlates evidence produced by investigation agents.
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

        grouped = self.group_by_service(
            state.evidence
        )

        correlations = []

        for service, evidence_list in grouped.items():

            correlation = self.build_correlation(
                service,
                evidence_list,
            )

            correlations.append(
                correlation
            )

        state.correlations = correlations

        state.timeline.append(
            f"Correlation Engine created {len(correlations)} correlations."
        )

        return state

    # ------------------------------------------------------------------
    # Group Evidence
    # ------------------------------------------------------------------

    def group_by_service(
        self,
        evidence: list[Evidence],
    ) -> dict[str, list[Evidence]]:

        grouped = defaultdict(list)

        for item in evidence:

            grouped[item.service_name].append(item)

        return grouped

    # ------------------------------------------------------------------
    # Build Correlation
    # ------------------------------------------------------------------

    def build_correlation(
        self,
        service: str,
        evidence: list[Evidence],
    ) -> Correlation:

        severity = self.highest_severity(
            evidence
        )

        confidence = self.average_confidence(
            evidence
        )

        causes = self.generate_causes(
            evidence
        )

        impacted = sorted(
            {
                item.service_name
                for item in evidence
            }
        )

        return Correlation(

            service_name=service,

            severity=severity,

            confidence=confidence,

            title=f"{service} Investigation",

            summary=(
                f"{len(evidence)} correlated evidence "
                f"items were detected for '{service}'."
            ),

            evidence=evidence,

            possible_causes=causes,

            impacted_services=impacted,

            evidence_count=len(evidence),

        )

    # ------------------------------------------------------------------
    # Highest Severity
    # ------------------------------------------------------------------

    def highest_severity(
        self,
        evidence: list[Evidence],
    ) -> str:

        highest = "LOW"

        for item in evidence:

            if (
                self.SEVERITY_PRIORITY[item.severity]
                >
                self.SEVERITY_PRIORITY[highest]
            ):
                highest = item.severity

        return highest

    # ------------------------------------------------------------------
    # Confidence
    # ------------------------------------------------------------------

    def average_confidence(
        self,
        evidence: list[Evidence],
    ) -> int:

        if not evidence:
            return 0

        return int(

            sum(
                item.confidence
                for item in evidence
            )

            / len(evidence)

        )

    # ------------------------------------------------------------------
    # AI Cause Generator
    # ------------------------------------------------------------------

    def generate_causes(
        self,
        evidence: list[Evidence],
    ) -> list[str]:

        causes = set()

        for item in evidence:

            if item.type == "Critical Slow API":

                causes.add(
                    "High API latency detected."
                )

            elif item.type == "Slow API":

                causes.add(
                    "Application response time increased."
                )

            elif item.type == "Server Error":

                causes.add(
                    "Application exceptions detected."
                )

            elif item.type == "Application Error":

                causes.add(
                    "Application log errors detected."
                )

            elif item.type == "High Traffic":

                causes.add(
                    "Traffic surge may be affecting the service."
                )

            elif item.type == "Dependency Failure":

                causes.add(
                    "Downstream dependency failures detected."
                )

            elif item.type == "Recurring Application Failure":

                causes.add(
                    "Historical incidents indicate a recurring failure."
                )

            elif item.type == "Active Alert":

                causes.add(
                    "Monitoring alerts confirm the incident."
                )

        if not causes:

            causes.add(
                "No obvious cause identified."
            )

        return sorted(causes)