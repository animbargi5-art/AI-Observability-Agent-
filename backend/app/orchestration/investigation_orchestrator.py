from app.agents.trace_agent import TraceAgent
from app.agents.logs_agent import LogsAgent
from app.agents.metrics_agent import MetricsAgent
from app.agents.dependency_agent import DependencyAgent
from app.agents.alert_agent import AlertAgent
from app.agents.historical_agent import HistoricalAgent

from app.agents.correlation_engine import CorrelationEngine
from app.graph.graph_builder import GraphBuilder

from app.agents.root_cause_agent import RootCauseAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.report_agent import ReportAgent

class InvestigationOrchestrator:

    def __init__(self, memory, coordinator):

        self.memory = memory

        self.coordinator = coordinator

        self.trace_agent = TraceAgent(memory)
        self.logs_agent = LogsAgent(memory)
        self.metrics_agent = MetricsAgent(memory)

        self.dependency_agent = DependencyAgent(memory)
        self.alert_agent = AlertAgent(memory)
        self.historical_agent = HistoricalAgent(memory)

        self.correlation_engine = CorrelationEngine(memory)
        self.graph_builder = GraphBuilder(memory)

        self.root_cause_agent = RootCauseAgent(memory)
        self.recommendation_agent = RecommendationAgent(memory)
        self.report_agent = ReportAgent(memory)

    def run(self):

        self.collect_evidence()

        self.coordinator.build_incident()

        self.correlate()

        self.build_graph()

        self.reason()

        self.find_root_cause()

        self.generate_recommendations()

        return self.generate_report()

    def collect_evidence(self):
        print("\n========== COLLECTING EVIDENCE ==========\n")

        results = {}

        results["trace"] = self.trace_agent.run()

        results["logs"] = self.logs_agent.run()

        results["metrics"] = self.metrics_agent.run()

        results["dependency"] = self.dependency_agent.run()

        results["alert"] = self.alert_agent.run()

        results["historical"] = self.historical_agent.run()

        return results

    def correlate(self):

        print("\n========== CORRELATING EVIDENCE ==========\n")

        return self.correlation_engine.run()

    def build_graph(self):

        print("\n========== BUILDING KNOWLEDGE GRAPH ==========\n")

        return self.graph_builder.build()

    def reason(self):

        print("\n========== REASONING ==========\n")

        return self.root_cause_agent.reasoning_engine.analyze()

    def find_root_cause(self):

        print("\n========== ROOT CAUSE ANALYSIS ==========\n")

        return self.root_cause_agent.run()

    def generate_recommendations(self):

        print("\n========== GENERATING RECOMMENDATIONS ==========\n")

        return self.recommendation_agent.run()

    def generate_report(self):

        print("\n========== GENERATING FINAL REPORT ==========\n")

        return self.report_agent.run()