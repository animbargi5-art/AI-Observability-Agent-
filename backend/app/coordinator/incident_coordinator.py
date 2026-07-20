from app.memory.investigation_memory import InvestigationMemory

from app.agents.trace_agent import TraceAgent
from app.agents.logs_agent import LogsAgent
from app.agents.metrics_agent import MetricsAgent
from app.agents.dependency_agent import DependencyAgent
from app.agents.alert_agent import AlertAgent
from app.agents.historical_agent import HistoricalAgent
from app.agents.root_cause_agent import RootCauseAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.report_agent import ReportAgent
from app.agents.correlation_engine import CorrelationEngine

class IncidentCoordinator:
    """
    Coordinates the complete AI investigation workflow.
    """

    def __init__(self):

        # One shared investigation memory
        self.memory = InvestigationMemory()

        self.trace_agent = TraceAgent(self.memory)
        self.logs_agent = LogsAgent(self.memory)
        self.metrics_agent = MetricsAgent(self.memory)

        self.dependency_agent = DependencyAgent(self.memory)
        self.alert_agent = AlertAgent(self.memory)
        self.historical_agent = HistoricalAgent(self.memory)

        self.correlation_engine = CorrelationEngine(self.memory)

        self.root_cause_agent = RootCauseAgent(self.memory)
        self.recommendation_agent = RecommendationAgent(self.memory)
        self.report_agent = ReportAgent(self.memory)

    def start_investigation(self):

        print("=" * 60)
        print("Starting New Investigation")
        print("=" * 60)

        results = {}

        results["trace"] = self.trace_agent.run()

        results["logs"] = self.logs_agent.run()

        results["metrics"] = self.metrics_agent.run()

        results["dependency"] = self.dependency_agent.run()

        results["alert"] = self.alert_agent.run()

        results["historical"] = self.historical_agent.run()

        self.build_incident()

        results["correlation"] = self.correlation_engine.run()

        results["root_cause"] = self.root_cause_agent.run()

        results["recommendation"] = self.recommendation_agent.run()

        results["report"] = self.report_agent.run()


        return {
            "memory": self.memory,
            "results": results
        }
    
    def build_incident(self):
        """
        Build the current incident from all collected evidence.
        """

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
