from app.agents.base_agent import BaseAgent
from app.tools.metrics_tool import MetricsTool
from app.memory.investigation_memory import InvestigationMemory


class MetricsAgent(BaseAgent):
    """
    Responsible for collecting and analyzing metrics.
    """

    def __init__(self, memory=None):

        super().__init__(
            name="Metrics Agent",
            description="Analyzes application metrics from SigNoz."
        )

        self.metrics_tool = MetricsTool()

        if memory is None:
            self.memory = InvestigationMemory()
        else:
            self.memory = memory

    def fetch_metrics(self):

        return self.metrics_tool.execute()

    def execute(self):

        metrics = self.fetch_metrics()

        if metrics.get("status") == "error":
            return {
                "total_metrics": 0,
                "findings": [],
                "error": metrics["message"]
            }

        return self.analyze(metrics)

    def analyze(self, metrics):

        findings = []

        # Future metric analysis logic will go here.
        # For now there are no findings because the
        # local SigNoz instance has no recent metrics.

        for finding in findings:
            self.memory.add_evidence(finding)

        self.memory.add_timeline_event(
            "Metrics investigation completed."
        )

        if findings:
            self.memory.set_confidence(88)

        return {
            "total_metrics": len(findings),
            "findings": findings
        }