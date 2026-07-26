"""
===============================================================================
TattvaAI - Alert Agent
===============================================================================

Purpose
-------
Analyzes active monitoring alerts and generates investigation evidence.

Responsibilities
----------------
• Retrieve active alerts
• Detect critical alerts
• Detect warning alerts
• Generate Evidence objects
• Update InvestigationState

Flow
----
InvestigationState
        ↓
AlertTool
        ↓
List[Alert]
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
from app.tools.alert_tool import AlertTool


class AlertAgent(BaseAgent):
    """
    AI agent responsible for alert investigation.
    """

    def __init__(self):

        super().__init__(
            name="Alert Agent",
            description="Analyzes monitoring alerts."
        )

        self.alert_tool = AlertTool()

    async def execute(
        self,
        state: InvestigationState,
    ) -> InvestigationState:

        self.log(
            f"Investigating alerts for {state.service_name}"
        )

        alerts = await self.alert_tool.execute()

        state.alerts = alerts

        highest_confidence = state.confidence

        for alert in alerts:

            evidence = self.analyze_alert(alert)

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
            f"Alert Agent analyzed {len(alerts)} alerts."
        )

        return state

    # ---------------------------------------------------------------------
    # Alert Analysis
    # ---------------------------------------------------------------------

    def analyze_alert(
        self,
        alert,
    ) -> Evidence | None:

        status = (alert.status or "").upper()
        severity = (alert.severity or "").upper()

        if status != "FIRING":
            return None

        confidence = 80

        if severity == "CRITICAL":

            confidence = 98

        elif severity == "HIGH":

            confidence = 90

        elif severity == "MEDIUM":

            confidence = 80

        else:

            confidence = 70

        return Evidence(

            source="alerts",

            category="Monitoring",

            type="Active Alert",

            severity=severity,

            confidence=confidence,

            service_name=alert.service_name,

            title=alert.name,

            summary=alert.description,

            recommendation=(
                "Review the triggering condition and correlate "
                "this alert with traces, logs and metrics."
            ),

            alert_id=alert.alert_id,

            timestamp=alert.timestamp,

            raw=alert.model_dump(),

        )