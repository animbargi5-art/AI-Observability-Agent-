from app.tools.logs_tool import LogsTool
from app.agents.base_agent import BaseAgent
from app.memory.investigation_memory import InvestigationMemory


class LogsAgent(BaseAgent):

    def __init__(self, memory=None):

        super().__init__(
            name="Logs Agent",
            description="Analyzes application logs and detects log-based incidents."
        )

        self.logs_tool = LogsTool()

        if memory is None:
            self.memory = InvestigationMemory()
        else:
            self.memory = memory

    def fetch_logs(self):

        return self.logs_tool.execute()

    def execute(self):

        logs = self.fetch_logs()

        return self.analyze(logs)

    def analyze(self, logs):

        print("\n========== LOGS RESPONSE ==========")
        print(logs)
        print("===================================\n")
        
        findings = []

        # Future log analysis logic will go here.
        # For now there are no log findings because
        # the local SigNoz instance has no logs.

        for finding in findings:
            self.memory.add_evidence(finding)

        self.memory.add_timeline_event(
            "Logs investigation completed."
        )

        if findings:
            self.memory.set_confidence(85)

        return {
            "total_logs": len(findings),
            "findings": findings
        }