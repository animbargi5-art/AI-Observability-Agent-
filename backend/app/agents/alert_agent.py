from app.agents.base_agent import BaseAgent
from app.tools.alert_tool import AlertTool
from app.memory.investigation_memory import InvestigationMemory


class AlertAgent(BaseAgent):

    def __init__(self, memory=None):

        super().__init__(
            "Alert Agent",
            "Analyzes active alerts from SigNoz."
        )

        self.alert_tool = AlertTool()

        if memory is None:
            self.memory = InvestigationMemory()
        else:
            self.memory = memory

    def fetch_alerts(self):

        return self.alert_tool.execute()

    def execute(self):

        result = self.fetch_alerts()

        alerts = result.get("alerts", [])

        findings = []

        for alert in alerts:

            findings.append({
                "name": alert.get("name"),
                "severity": alert.get("severity"),
                "status": alert.get("status"),
                "service": alert.get("service")
            })

        # Store evidence
        for finding in findings:
            self.memory.add_evidence(finding)

        # Timeline
        self.memory.add_timeline_event(
            "Alert investigation completed."
        )

        # Temporary confidence
        if findings:
            self.memory.set_confidence(85)

        return {
            "total_alerts": len(findings),
            "findings": findings
        }