import json

from mcp.types import TextContent

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

    async def fetch_logs(self):

        return await self.logs_tool.execute()

    async def execute(self):

        logs = await self.fetch_logs()

        print("\n========== LOG RAW RESPONSE ==========")
        print(type(logs))
        print("======================================")

        payload = {}

        if hasattr(logs, "content"):

            for item in logs.content:

                if isinstance(item, TextContent):

                    try:

                        payload = json.loads(item.text)

                        break

                    except Exception as ex:

                        print("JSON Parse Error:", ex)

        print("Payload Keys:", payload.keys())

        return self.analyze(payload)

    def analyze(self, logs):

        print("Payload Keys:", logs.keys())

        rows = (
            logs.get("data", {})
                .get("data", {})
                .get("results", [{}])[0]
                .get("rows", [])
        )

        print(f"Rows Found: {len(rows)}")

        if rows:

            print("\n========== FIRST LOG ==========")
            print(json.dumps(rows[0], indent=4))
            print("================================\n")

        else:

            print("No log rows returned.")

        findings = []

        for row in rows:

            data = row.get("data", {})

            body = data.get("body", "")
            body_lower = body.lower()

            # Ignore MCP communication
            if "localhost:8001/mcp" in body_lower:
                continue

            # Ignore investigation endpoint
            if "/investigation/start" in body_lower:
                continue

            # Ignore httpx debug logs
            if body.startswith("HTTP Request"):
                continue

            severity = (
                data.get("severity_text", "")
                .upper()
            )

            timestamp = row.get("timestamp")

            service = (
                data.get("resources_string", {})
                    .get("service.name")
            )

            trace_id = data.get("trace_id")

            span_id = data.get("span_id")

            if severity == "ERROR":

                findings.append({

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

                })

            elif severity in ["WARN", "WARNING"]:

                findings.append({

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

                })

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

        print("\n========== LOG AGENT FINISHED ==========")
        print(f"Logs     : {len(rows)}")
        print(f"Findings : {len(findings)}")
        print("========================================\n")

        return {

            "total_logs": len(rows),

            "findings": findings

        }