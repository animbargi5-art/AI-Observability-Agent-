"""
===============================================================================
TattvaAI - Trace Agent
===============================================================================

Purpose
-------
Analyzes distributed traces collected from SigNoz and generates
investigation evidence.

Responsibilities
----------------
• Retrieve normalized traces
• Detect slow APIs
• Detect HTTP errors
• Generate Evidence objects
• Update InvestigationState

Flow
----
InvestigationState
        ↓
TraceTool
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
from app.tools.trace_tool import TraceTool


class TraceAgent(BaseAgent):
    """
    AI agent responsible for trace investigation.
    """

    CRITICAL_THRESHOLD = 1000
    WARNING_THRESHOLD = 500
    HEALTHY_THRESHOLD = 200

    def __init__(self):

        super().__init__(
            name="Trace Agent",
            description="Analyzes distributed traces."
        )

        self.trace_tool = TraceTool()

    async def execute(
        self,
        state: InvestigationState,
    ) -> InvestigationState:

        self.log(
            f"Investigating traces for {state.service_name}"
        )

        traces = await self.trace_tool.execute(
            service_name=state.service_name
        )

        state.traces = traces

        highest_confidence = state.confidence

        for trace in traces:

            evidence = self.analyze_trace(trace)

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
            f"Trace Agent analyzed {len(traces)} traces."
        )

        return state

    # -----------------------------------------------------------------

    def analyze_trace(
        self,
        trace,
    ) -> Evidence | None:

        severity = None
        evidence_type = None
        confidence = 0

        # ---------------------------------------------------------
        # Performance
        # ---------------------------------------------------------

        if trace.duration_ms >= self.CRITICAL_THRESHOLD:

            severity = "HIGH"
            evidence_type = "Critical Slow API"
            confidence = 95

        elif trace.duration_ms >= self.WARNING_THRESHOLD:

            severity = "MEDIUM"
            evidence_type = "Slow API"
            confidence = 85

        elif trace.duration_ms >= self.HEALTHY_THRESHOLD:

            severity = "LOW"
            evidence_type = "Performance Warning"
            confidence = 70

        # ---------------------------------------------------------
        # HTTP Status
        # ---------------------------------------------------------

        if trace.failed:

            severity = "CRITICAL"
            evidence_type = "Server Error"
            confidence = 98

        elif trace.client_error:

            severity = "MEDIUM"
            evidence_type = "Client Error"
            confidence = 80

        if evidence_type is None:
            return None

        return Evidence(

            source="trace",

            category="Performance",

            type=evidence_type,

            severity=severity,

            confidence=confidence,

            service_name=trace.service_name,

            endpoint=trace.endpoint,

            operation=trace.operation_name,

            title=evidence_type,

            summary=(
                f"{trace.operation_name} "
                f"took {trace.duration_ms:.2f} ms "
                f"with status {trace.status_code}"
            ),

            trace_id=trace.trace_id,

            span_id=trace.span_id,

            timestamp=trace.timestamp,

            raw=trace.model_dump(),

        )