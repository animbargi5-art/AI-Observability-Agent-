"""
===============================================================================
TattvaAI - Historical Agent
===============================================================================

Purpose
-------
Analyzes previous incidents and generates investigation evidence.

Responsibilities
----------------
• Retrieve historical incidents
• Detect recurring failures
• Generate Evidence objects
• Update InvestigationState

Flow
----
InvestigationState
        ↓
HistoricalTool
        ↓
List[HistoricalIncident]
        ↓
Evidence
        ↓
InvestigationState

===============================================================================
"""

from __future__ import annotations

from app.agents.base_agent import BaseAgent

from app.models.evidence import Evidence
from app.models.historical_incident import HistoricalIncident

from app.schemas.investigation_state import InvestigationState

from app.tools.historical_tool import HistoricalTool


class HistoricalAgent(BaseAgent):
    """
    AI Agent responsible for historical incident analysis.
    """

    def __init__(self):

        super().__init__(

            name="Historical Agent",

            description="Analyzes historical incidents."

        )

        self.history_tool = HistoricalTool()

    # -------------------------------------------------------------------------
    # Execute
    # -------------------------------------------------------------------------

    async def execute(
        self,
        state: InvestigationState,
    ) -> InvestigationState:

        self.log(

            f"Searching historical incidents for "

            f"{state.service_name}"

        )

        incidents = await self.history_tool.execute(

            service_name=state.service_name,

        )

        state.historical_incidents = incidents

        highest_confidence = state.confidence

        for incident in incidents:

            evidence = self.analyze_incident(

                incident

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

            f"Historical Agent analyzed "

            f"{len(incidents)} historical incident(s)."

        )

        return state

    # -------------------------------------------------------------------------
    # Analysis
    # -------------------------------------------------------------------------

    def analyze_incident(
        self,
        incident: HistoricalIncident,
    ) -> Evidence | None:

        if incident.occurrence_count <= 1:

            return None

        severity = incident.severity.upper()

        confidence = min(

            70 + (incident.occurrence_count * 5),

            95,

        )

        return Evidence(

            source="history",

            category="Historical",

            type="Recurring Incident",

            severity=severity,

            confidence=confidence,

            service_name=incident.service_name,

            endpoint=incident.endpoint,

            title=incident.title,

            summary=(

                f"Incident has occurred "

                f"{incident.occurrence_count} times. "

                f"Previous root cause: "

                f"{incident.root_cause}"

            ),

            recommendation=(

                "Review previous investigation and "

                "verify whether the same root cause "

                "still exists."

            ),

            timestamp=incident.resolved_at,

            raw=incident.model_dump(),

        )