import json

from mcp.types import TextContent

from app.agents.base_agent import BaseAgent
from app.tools.trace_tool import TraceTool
from app.memory.investigation_memory import InvestigationMemory


HEALTHY_THRESHOLD = 200
WARNING_THRESHOLD = 500
SLOW_API_THRESHOLD = 1000


class TraceAgent(BaseAgent):
    """
    AI Agent responsible for fetching and analyzing traces
    from SigNoz.
    """

    def __init__(self, memory=None):

        super().__init__(
            name="Trace Investigation Agent",
            description="Fetches and analyzes distributed traces from SigNoz."
        )

        self.trace_tool = TraceTool()

        if memory is None:
            self.memory = InvestigationMemory()
        else:
            self.memory = memory

    async def fetch_traces(self):
        return await self.trace_tool.execute()

    async def execute(self):

        traces = await self.fetch_traces()

        print("\n========== TRACE RAW RESPONSE ==========")
        print(type(traces))
        print(traces)
        print("========================================\n")

        payload = {}

        if hasattr(traces, "content"):

            for item in traces.content:

                if isinstance(item, TextContent):

                    try:

                        payload = json.loads(item.text)

                        break

                    except Exception as ex:

                        print("JSON Parse Error:", ex)

        print("\n========== TRACE PAYLOAD ==========")
        print(type(payload))
        print(payload)
        print("===================================\n")

        rows = (
            payload.get("data", {})
                   .get("data", {})
                   .get("results", [{}])[0]
                   .get("rows", [])
        )

        incidents = []

        for row in rows:

            data = row.get("data", {})

            incidents.append({

                "service": data.get("service.name"),

                "endpoint": data.get("name"),

                "method": data.get("http_method"),

                "status": data.get("response_status_code"),

                "duration_ms": round(
                    data.get("duration_nano", 0) / 1_000_000,
                    2
                ),

                "trace_id": data.get("trace_id"),

                "timestamp": data.get("timestamp")

            })

        findings = self.detect_incidents(incidents)

        for finding in findings:
            self.memory.add_evidence(finding)

        self.memory.add_timeline_event(
            "Trace investigation completed."
        )

        if findings:

            highest_confidence = max(
                finding["confidence"]
                for finding in findings
            )

            self.memory.set_confidence(highest_confidence)

        return {

            "total_traces": len(incidents),

            "incidents_found": len(findings),

            "findings": findings

        }

    def detect_incidents(self, incidents):

        findings = []

        for incident in incidents:

            duration = incident["duration_ms"]

            status = str(incident["status"])

            if duration > SLOW_API_THRESHOLD:

                findings.append({

                    "severity": "HIGH",

                    "confidence": 95,

                    "category": "Performance",

                    "root_service": incident["service"],

                    "type": "Critical Slow API",

                    "message": (
                        f"{incident['endpoint']} took "
                        f"{duration:.2f} ms"
                    ),

                    "trace": incident

                })

            elif duration > WARNING_THRESHOLD:

                findings.append({

                    "severity": "MEDIUM",

                    "confidence": 85,

                    "category": "Performance",

                    "root_service": incident["service"],

                    "type": "Slow API",

                    "message": (
                        f"{incident['endpoint']} took "
                        f"{duration:.2f} ms"
                    ),

                    "trace": incident

                })

            elif duration > HEALTHY_THRESHOLD:

                findings.append({

                    "severity": "LOW",

                    "confidence": 70,

                    "category": "Performance",

                    "root_service": incident["service"],

                    "type": "Performance Warning",

                    "message": (
                        f"{incident['endpoint']} took "
                        f"{duration:.2f} ms"
                    ),

                    "trace": incident

                })

            if status.startswith("5"):

                findings.append({

                    "severity": "CRITICAL",

                    "confidence": 98,

                    "category": "Application",

                    "root_service": incident["service"],

                    "type": "Server Error",

                    "message": (
                        f"{incident['endpoint']} returned {status}"
                    ),

                    "trace": incident

                })

            if status.startswith("4"):

                findings.append({

                    "severity": "MEDIUM",

                    "confidence": 80,

                    "category": "Application",

                    "root_service": incident["service"],

                    "type": "Client Error",

                    "message": (
                        f"{incident['endpoint']} returned {status}"
                    ),

                    "trace": incident

                })

        return findings