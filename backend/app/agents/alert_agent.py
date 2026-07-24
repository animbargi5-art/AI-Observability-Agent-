import json

from mcp.types import TextContent

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

    async def fetch_alerts(self):

        return await self.alert_tool.execute()

    async def execute(self):

        result = await self.fetch_alerts()

        payload = {}

        for item in result.content:

            if isinstance(item, TextContent):

                try:
                    payload = json.loads(item.text)
                    break

                except Exception:
                    pass

        # Temporary debugging
        print("\n========== ALERT PAYLOAD ==========")
        print(payload)
        print("===================================\n")

        # Stop here until we know the JSON structure
        return {
            "status": "STOP",
            "payload": payload
        }

    def analyze(self, alerts):

        findings = []

        for alert in alerts:

            findings.append({
                "name": alert.get("name"),
                "severity": alert.get("severity"),
                "status": alert.get("status"),
                "service": alert.get("service")
            })

        for finding in findings:
            self.memory.add_evidence(finding)

        self.memory.add_timeline_event(
            "Alert investigation completed."
        )

        if findings:
            self.memory.set_confidence(85)

        return {
            "total_alerts": len(findings),
            "findings": findings
        }