from datetime import datetime
import time

from app.services.investigation_service import InvestigationService
from app.memory.investigation_memory import InvestigationMemory
from app.orchestration.investigation_orchestrator import InvestigationOrchestrator
from app.services.telemetry_service import TelemetryService


class IncidentCoordinator:
    """
    Coordinates the complete AI investigation workflow.
    """

    def __init__(self):

        self.memory = InvestigationMemory()

        self.orchestrator = InvestigationOrchestrator(
            self.memory,
            self
        )

        self.investigation_service = InvestigationService()

        self.telemetry_service = TelemetryService()

    def start_investigation(self):

        print("=" * 60)
        print("Starting New Investigation")
        print("=" * 60)

        start_time = time.time()

        traces = self.telemetry_service.get_traces()

        metrics = self.telemetry_service.get_metrics()

        logs = self.telemetry_service.get_logs()

        print(f"Collected {len(traces)} traces")

        print(f"Collected {len(metrics)} metrics")

        print(f"Collected {len(logs)} logs")

        report = self.orchestrator.run()

        saved = self.investigation_service.save(report)

        execution_time = round(
            time.time() - start_time,
            3
        )

        print("\n========== DATABASE ==========")

        print(f"Saved Investigation ID : {saved.id}")

        print("==============================\n")

        return {

            "status": "SUCCESS",

            "timestamp": datetime.utcnow().isoformat(),

            "execution_time_seconds": execution_time,

            "report": report,

            "memory": self.memory

        }

    def build_incident(self):

        evidence = self.memory.evidence

        if not evidence:

            self.memory.set_incident({

                "id": "INC-000",

                "title": "No active incident",

                "severity": "NONE",

                "status": "NO_ISSUE",

                "evidence_count": 0

            })

            return

        highest = max(

            evidence,

            key=lambda x: {

                "LOW": 1,

                "MEDIUM": 2,

                "HIGH": 3,

                "CRITICAL": 4

            }.get(x.get("severity", "LOW"), 1)

        )

        incident = {

            "id": "INC-001",

            "title": highest.get("type", "Unknown Incident"),

            "severity": highest.get("severity", "LOW"),

            "status": "INVESTIGATING",

            "evidence_count": len(evidence)

        }

        self.memory.set_incident(incident)