"""Canonical coordinator for the TattvaAI investigation lifecycle."""

from __future__ import annotations

from datetime import datetime
from time import perf_counter
from uuid import uuid4

from app.agents.report_agent import ReportAgent
from app.core.settings import settings
from app.decision.investigation_engine import InvestigationEngine
from app.models.evidence import Evidence
from app.schemas.investigation_state import InvestigationState
from app.services.investigation_service import InvestigationService


class IncidentCoordinator:
    """Runs one evidence-first investigation and persists its final report."""

    def __init__(self) -> None:
        self.investigation_engine = InvestigationEngine()
        self.report_agent = ReportAgent()
        self.investigation_service = InvestigationService()

    async def start_investigation(self, service_name: str = "gateway") -> dict:
        started_at = datetime.utcnow()
        started = perf_counter()
        incident_id = f"INC-{uuid4().hex[:8].upper()}"
        state = InvestigationState(
            incident_id=incident_id,
            service_name=service_name,
            incident={
                "id": incident_id,
                "title": f"Investigation for {service_name}",
                "status": "INVESTIGATING",
                "severity": "LOW",
            },
        )

        if settings.DEMO_MODE:
            state.evidence = self._demo_evidence(service_name, incident_id)
            state.timeline.append("Demo telemetry loaded for local investigation.")
        else:
            raise RuntimeError(
                "Live SigNoz collection is not configured. Set DEMO_MODE=true "
                "for the demo or configure the MCP gateway before investigating."
            )

        state.confidence = max(item.confidence for item in state.evidence)
        state = self.investigation_engine.execute(state)
        state.reasoning["graph"] = self._build_graph(state)
        state.incident.update({
            "title": f"{state.service_name} service degradation",
            "status": "COMPLETED",
            "severity": state.reasoning["highest_severity"],
        })
        state = await self.report_agent.run(state)
        report = state.final_report
        report.started_at = started_at
        report.completed_at = datetime.utcnow()
        report.investigation_duration_seconds = round(perf_counter() - started, 3)
        report.refresh_statistics()
        saved = self.investigation_service.save(report)

        return {
            "status": "SUCCESS",
            "investigation_id": saved.id,
            "incident_id": incident_id,
            "execution_time_seconds": report.investigation_duration_seconds,
            "report": report.model_dump(mode="json"),
        }

    @staticmethod
    def _demo_evidence(service_name: str, incident_id: str) -> list[Evidence]:
        now = datetime.utcnow()
        common = {"service_name": service_name, "investigation_id": incident_id, "timestamp": now}
        return [
            Evidence(source="traces", agent_name="Trace Agent", category="Performance", type="Critical Slow API", severity="HIGH", confidence=94, title="Checkout latency spike", summary="POST /checkout exceeded 2.4 seconds.", endpoint="/checkout", operation="POST /checkout", recommendation="Inspect downstream payment latency.", **common),
            Evidence(source="logs", agent_name="Logs Agent", category="Application", type="Application Error", severity="CRITICAL", confidence=98, title="Payment timeout", summary="TimeoutException while calling payment service.", recommendation="Review payment service availability and timeout policy.", **common),
            Evidence(source="metrics", agent_name="Metrics Agent", category="Application", type="High Error Rate", severity="CRITICAL", confidence=97, title="Error rate above threshold", summary="5xx error rate reached 12.4%.", metric_name="http.server.error_rate", recommendation="Mitigate the failing dependency and monitor recovery.", **common),
            Evidence(source="alerts", agent_name="Alert Agent", category="Monitoring", type="Active Alert", severity="HIGH", confidence=90, title="Gateway error rate alert", summary="Error-rate alert is firing for the gateway.", alert_id="demo-gateway-error-rate", recommendation="Confirm the alert against traces and logs.", **common),
        ]

    @staticmethod
    def _build_graph(state: InvestigationState) -> dict:
        nodes = [
            {"id": "incident", "label": state.incident["title"], "type": "incident"},
            *[
                {"id": f"evidence-{index}", "label": item.title, "type": "evidence"}
                for index, item in enumerate(state.evidence)
            ],
        ]
        edges = [
            {"source": "incident", "target": f"evidence-{index}", "relation": "supported_by"}
            for index, _ in enumerate(state.evidence)
        ]
        return {"nodes": nodes, "edges": edges}
