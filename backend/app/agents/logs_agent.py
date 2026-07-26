"""
===============================================================================
TattvaAI - Logs Agent
===============================================================================

Purpose
-------
Analyzes application logs and converts them into investigation evidence.

Responsibilities
----------------
• Retrieve normalized logs
• Detect application errors
• Detect warnings
• Detect critical failures
• Generate Evidence objects
• Update InvestigationState

Flow
----
InvestigationState
        ↓
LogsTool
        ↓
Log
        ↓
Evidence
        ↓
InvestigationState

===============================================================================
"""

from __future__ import annotations

from app.agents.base_agent import BaseAgent

from app.models.log import Log
from app.models.evidence import Evidence

from app.schemas.investigation_state import InvestigationState

from app.tools.logs_tool import LogsTool


class LogsAgent(BaseAgent):
    """
    AI agent responsible for log analysis.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Logs Agent",
            description="Analyzes application logs.",
        )

        self.logs_tool = LogsTool()

    # -------------------------------------------------------------------------
    # Execute
    # -------------------------------------------------------------------------

    async def execute(
        self,
        state: InvestigationState,
    ) -> InvestigationState:

        self.log(
            f"Collecting logs for '{state.service_name}'."
        )

        logs = await self.logs_tool.execute(
            service_name=state.service_name,
        )

        state.logs = logs

        highest_confidence = state.confidence

        for log in logs:

            evidence = self.analyze_log(log)

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
            f"Logs Agent analyzed {len(logs)} log(s).",
        )

        return state

    # -------------------------------------------------------------------------
    # Log Analysis
    # -------------------------------------------------------------------------

    def analyze_log(
        self,
        log: Log,
    ) -> Evidence | None:

        level = (log.severity or "").upper()

        if level == "ERROR":

            return self.create_evidence(
                log=log,
                evidence_type="Application Error",
                severity="HIGH",
                confidence=95,
                recommendation=(
                    "Review stack trace, recent deployments, "
                    "and related distributed traces."
                ),
            )

        if level == "WARN":

            return self.create_evidence(
                log=log,
                evidence_type="Application Warning",
                severity="MEDIUM",
                confidence=80,
                recommendation=(
                    "Inspect warning patterns before they become failures."
                ),
            )

        if level == "FATAL":

            return self.create_evidence(
                log=log,
                evidence_type="Critical Failure",
                severity="CRITICAL",
                confidence=99,
                recommendation=(
                    "Immediate investigation required. "
                    "Check application health and dependencies."
                ),
            )

        return None

    # -------------------------------------------------------------------------
    # Evidence Builder
    # -------------------------------------------------------------------------

    def create_evidence(
        self,
        log: Log,
        evidence_type: str,
        severity: str,
        confidence: int,
        recommendation: str,
    ) -> Evidence:

        return Evidence(

            source="logs",

            category="Application",

            type=evidence_type,

            severity=severity,

            confidence=confidence,

            service_name=log.service_name,

            endpoint=getattr(log, "endpoint", None),

            title=evidence_type,

            summary=log.message,

            recommendation=recommendation,

            trace_id=getattr(log, "trace_id", None),

            span_id=getattr(log, "span_id", None),

            timestamp=log.timestamp,

            raw=log.model_dump(),

        )