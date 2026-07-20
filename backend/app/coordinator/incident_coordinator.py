from app.memory.investigation_memory import InvestigationMemory

from app.agents.trace_agent import TraceAgent
from app.agents.logs_agent import LogsAgent
from app.agents.metrics_agent import MetricsAgent
from app.agents.dependency_agent import DependencyAgent
from app.agents.alert_agent import AlertAgent
from app.agents.historical_agent import HistoricalAgent


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

        return {
            "memory": self.memory,
            "results": results
        }
