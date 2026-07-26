"""
===============================================================================
TattvaAI - Dependency Agent
===============================================================================

Purpose
-------
Analyzes service dependencies and generates investigation evidence.

Responsibilities
----------------
• Retrieve service dependencies
• Detect unhealthy downstream services
• Detect high dependency latency
• Generate Evidence objects
• Update InvestigationState

Flow
----
InvestigationState
        ↓
DependencyTool
        ↓
List[Dependency]
        ↓
Evidence
        ↓
InvestigationState

===============================================================================
"""

from __future__ import annotations

from app.agents.base_agent import BaseAgent
from app.models.dependency import Dependency
from app.models.evidence import Evidence
from app.schemas.investigation_state import InvestigationState
from app.tools.dependency_tool import DependencyTool


class DependencyAgent(BaseAgent):
    """
    AI agent responsible for dependency analysis.
    """

    def __init__(self):

        super().__init__(
            name="Dependency Agent",
            description="Analyzes service dependencies.",
        )

        self.dependency_tool = DependencyTool()

    # -------------------------------------------------------------------------
    # Execute
    # -------------------------------------------------------------------------

    async def execute(
        self,
        state: InvestigationState,
    ) -> InvestigationState:

        self.log(
            f"Analyzing dependencies for {state.service_name}"
        )

        dependencies = await self.dependency_tool.execute(
            service_name=state.service_name,
        )

        state.dependencies = dependencies

        highest_confidence = state.confidence

        for dependency in dependencies:

            evidence = self.analyze_dependency(
                dependency
            )

            if evidence is None:
                continue

            self.add_evidence(
                state,
                evidence,
            )

            highest_confidence = max(
                highest_confidence,
                evidence.confidence,
            )

        self.set_confidence(
            state,
            highest_confidence,
        )

        self.add_timeline(
            state,
            f"Dependency Agent analyzed {len(dependencies)} dependencies.",
        )

        return state

    # -------------------------------------------------------------------------
    # Dependency Analysis
    # -------------------------------------------------------------------------

    def analyze_dependency(
        self,
        dependency: Dependency,
    ) -> Evidence | None:

        if (
            dependency.error_rate <= 0
            and dependency.average_latency_ms < 1000
        ):
            return None

        severity = "MEDIUM"
        confidence = 80
        summary = []

        if dependency.error_rate > 0:

            severity = "HIGH"
            confidence = 95

            summary.append(
                f"Dependency error rate is {dependency.error_rate}%."
            )

        if dependency.average_latency_ms >= 1000:

            severity = "HIGH"

            confidence = max(confidence, 90)

            summary.append(
                f"Dependency latency reached "
                f"{dependency.average_latency_ms} ms."
            )

        return Evidence(

            source="dependency",

            category="Infrastructure",

            type="Dependency Failure",

            severity=severity,

            confidence=confidence,

            service_name=dependency.source_service,

            title=f"{dependency.target_service} Dependency",

            summary=" ".join(summary),

            recommendation=(
                "Inspect downstream service health, "
                "network latency and retry policies."
            ),

            raw=dependency.model_dump(),

        )