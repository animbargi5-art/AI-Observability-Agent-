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

        print("\n========== LOGS ==========")
        print(logs)

        return self.analyze(logs)

    def analyze(self, logs):

        rows = (
            logs.get("data", {})
                .get("data", {})
                .get("results", [{}])[0]
                .get("rows", [])
        )

        if rows is None:
            rows = []

        findings = []

        for row in rows:

            data = row["data"]

            body = data.get("body", "")
            severity = data.get("severity_text", "")
            severity = severity.upper()
            timestamp = row.get("timestamp")

            service = (
                data.get("resources_string", {})
                    .get("service.name")
            )

            trace_id = data.get("trace_id")

            span_id = data.get("span_id")

            if severity == "ERROR":

                findings.append(
                    {
                        "severity": "CRITICAL",
                        "confidence": 98,
                        "type": "Application Error",
                        "category": "Application",
                        "root_service": service,
                        "message": body,
                        "trace": {
                            "service": service,
                            "endpoint": "Log Event",
                            "status": "ERROR",
                            "trace_id": trace_id,
                            "span_id": span_id,
                            "timestamp": timestamp,
                        },
                    }
                )
            
            elif severity == "WARN":

                findings.append(
                    {
                        "severity": "HIGH",
                        "confidence": 90,
                        "type": "Performance Warning",
                        "category": "Application",
                        "root_service": service,
                        "message": body,
                        "trace": {
                            "service": service,
                            "endpoint": "Log Event",
                            "status": "WARN",
                            "trace_id": trace_id,
                            "span_id": span_id,
                            "timestamp": timestamp,
                        },
                    }
                ) 

        for finding in findings:
            self.memory.add_evidence(finding)

        self.memory.add_timeline_event(
            "Logs investigation completed."
        )

        if findings:
            highest_confidence = max(
                finding["confidence"]
                for finding in findings
            )
            self.memory.set_confidence(highest_confidence)

        return {
            "total_logs": len(rows),
            "findings": findings
        }