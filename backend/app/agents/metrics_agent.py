from app.agents.base_agent import BaseAgent
from app.tools.metrics_tool import MetricsTool
from app.memory.investigation_memory import InvestigationMemory

HIGH_TRAFFIC_THRESHOLD = 30
MEDIUM_TRAFFIC_THRESHOLD = 15

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

        results = (
            metrics
                .get("data", {})
                .get("data", {})
                .get("results", [])
        )

        if not results:
            return {
                "total_metrics": 0,
                "findings": []
            }

        aggregations = results[0].get("aggregations", [])

        if not aggregations:
            return {
                "total_metrics": 0,
                "findings": []
            }

        series = aggregations[0].get("series", [])

        if not series:
            return {
                "total_metrics": 0,
                "findings": []
            }

        values = series[0].get("values", [])

        for point in values:

            value = point.get("value", 0)

            timestamp = point.get("timestamp")

            if value >= HIGH_TRAFFIC_THRESHOLD:

                findings.append({

                    "severity": "HIGH",

                    "type": "High Traffic",

                    "confidence": 90,

                    "message": f"HTTP request rate reached {value}",

                    "category": "Infrastructure",

                    "root_service": "tattva-ai-backend",

                    "metric": {
                        "name": "HTTP Request Rate",
                        "value": value,
                        "timestamp": timestamp
                    }

                })

            elif value >= MEDIUM_TRAFFIC_THRESHOLD:

                findings.append({

                    "severity": "MEDIUM",

                    "type": "Traffic Spike",

                    "confidence": 75,

                    "message": f"HTTP request rate increased to {value}",

                    "category": "Infrastructure",

                    "root_service": "tattva-ai-backend",

                    "metric": {
                        "name": "HTTP Request Rate",
                        "value": value,
                        "timestamp": timestamp
                    }
                })

        for finding in findings:
            self.memory.add_evidence(finding)

        self.memory.add_timeline_event(
            "Metrics investigation completed."
        )

        if findings:

            highest_confidence = max(
                finding["confidence"]
                for finding in findings
            )
            self.memory.set_confidence(highest_confidence)

        return {
            "total_metrics": len(findings),
            "findings": findings
        }