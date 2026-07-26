"""
===============================================================================
TattvaAI - Historical Agent
===============================================================================

Purpose
-------
Analyzes historical telemetry and previous incidents to identify recurring
patterns and generate investigation evidence.

Responsibilities
----------------
• Retrieve historical traces
• Compare current and historical incidents
• Detect recurring failures
• Generate Evidence objects
• Update InvestigationState

Flow
----
InvestigationState
        ↓
HistoricalTool
        ↓
List[Trace]
        ↓
Evidence
        ↓
InvestigationState

===============================================================================
"""

from __future__ import annotations

from app.agents.base_agent import BaseAgent
from app.models.evidence import Evidence
from app.schemas.investigation_state import InvestigationState
from app.tools.historical_tool import HistoricalTool


class HistoricalAgent(BaseAgent):
    """
    AI agent responsible for historical incident analysis.
    """

    def __init__(self):

        super().__init__(
            name="Historical Agent",
            description="Analyzes historical telemetry."
        )

        self.history_tool = HistoricalTool()

    async def execute(
        self,
        state: InvestigationState,
    ) -> InvestigationState:

        self.log(
            f"Searching historical incidents for {state.service_name}"
        )

        history = await self.history_tool.execute(
            service_name=state.service_name,
        )

        state.historical_incidents = history

        highest_confidence = state.confidence

        for trace in history:

            evidence = self.analyze_history(trace)

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
            f"Historical Agent analyzed {len(history)} historical traces."
        )

        return state

    # -----------------------------------------------------------------
    # Historical Analysis
    # -----------------------------------------------------------------

    def analyze_history(
        self,
        trace,
    ) -> Evidence | None:

        if not trace.slow and not trace.failed:
            return None

        if trace.failed:

            evidence_type = "Recurring Application Failure"

            severity = "HIGH"

            confidence = 92

            summary = (
                f"Historical trace shows repeated server failures "
                f"for '{trace.operation_name}'."
            )

        else:

            evidence_type = "Recurring Performance Issue"

            severity = "MEDIUM"

            confidence = 80

            summary = (
                f"Historical trace indicates repeated latency "
                f"on '{trace.operation_name}'."
            )

        return Evidence(

            source="history",

            category="Historical",

            type=evidence_type,

            severity=severity,

            confidence=confidence,

            service_name=trace.service_name,

            endpoint=trace.endpoint,

            operation=trace.operation_name,

            title=evidence_type,

            summary=summary,

            recommendation=(
                "Compare current deployment with previous incidents "
                "and review recurring failure patterns."
            ),

            trace_id=trace.trace_id,

            span_id=trace.span_id,

            timestamp=trace.timestamp,

            raw=trace.model_dump(),

        )