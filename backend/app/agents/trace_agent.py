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

        payload = {}

        if hasattr(traces, "content"):

            for item in traces.content:

                if isinstance(item, TextContent):

                    try:
                        payload = json.loads(item.text)
                        break

                    except Exception as e:
                        print(f"JSON Parse Error: {e}")

        rows = (
            payload.get("data", {})
                   .get("data", {})
                   .get("results", [{}])[0]
                   .get("rows", [])
        )

        print(f"Trace rows received: {len(rows)}")

        incidents = []

        for row in rows:

            data = row.get("data", {})

            print("\n----------------------------")
            print("Service :", data.get("service.name"))
            print("Endpoint:", data.get("name"))
            print("Method  :", data.get("http_method"))
            print("Status  :", data.get("response_status_code"))
            print("----------------------------")

            endpoint = data.get("name", "")
            service = data.get("service.name", "")

            # --------------------------------------------------
            # Ignore internal telemetry
            # --------------------------------------------------

            if not endpoint:
                continue

            if endpoint.startswith("POST /investigation"):
                continue

            if endpoint.endswith("http send"):
                continue

            if "mcp" in endpoint.lower():
                continue

            if service == "tattva-ai-backend" and endpoint.endswith("http send"):
                continue

            incidents.append({

                "service": service,

                "endpoint": endpoint,

                "method": (
                    data.get("http_method")
                    or data.get("http.request.method")
                    or ""
                ),

                "status": (
                    data.get("response_status_code")
                    or data.get("http.response.status_code")
                    or ""
                ),

                "duration_ms": round(
                    data.get("duration_nano", 0) / 1_000_000,
                    2
                ),

                "trace_id": data.get("trace_id"),

                "timestamp": (
                    data.get("timestamp")
                    or row.get("timestamp")
                )

            })

        print(f"Valid incidents: {len(incidents)}")

        findings = self.detect_incidents(incidents)

        print(f"Findings generated: {len(findings)}")

        for finding in findings:
            self.memory.add_evidence(finding)

        self.memory.add_timeline_event(
            "Trace investigation completed."
        )

        if findings:

            self.memory.set_confidence(

                max(
                    finding["confidence"]
                    for finding in findings
                )

            )

        return {

            "total_traces": len(incidents),

            "incidents_found": len(findings),

            "findings": findings

        }

    def detect_incidents(self, incidents):

        findings = []

        for incident in incidents:

            duration = incident.get("duration_ms", 0)

            status = str(
                incident.get("status", "")
            )

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

            elif status.startswith("4"):

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