from app.agents.base_agent import BaseAgent
from app.decision.reasoning_engine import ReasoningEngine


class ReportAgent(BaseAgent):

    def __init__(self, memory):

        super().__init__(
            name="Report Agent",
            description="Generates the final investigation report."
        )

        self.memory = memory
        self.reasoning_engine = ReasoningEngine(memory)

    async def execute(self):

        reasoning = self.reasoning_engine.analyze()

        executive_summary = {

            "incident_title": self.memory.incident.get(
                "title",
                "Unknown Incident"
            ),

            "severity": self.memory.incident.get(
                "severity",
                "UNKNOWN"
            ),

            "confidence": self.memory.confidence,

            "highest_severity": reasoning.get(
                "highest_severity"
            ),

            "status": self.memory.incident.get(
                "status",
                "UNKNOWN"
            )

        }

        graph = self.memory.graph
        evidence = self.memory.evidence
        recommendations = self.memory.recommendations
        correlations = self.memory.correlations
        timeline = self.memory.timeline

        statistics = {

            "evidence_count": len(evidence),

            "recommendation_count": len(recommendations),

            "correlation_count": len(correlations),

            "timeline_events": len(timeline)

        }

        report = {

            "executive_summary": executive_summary,

            "statistics": statistics,

            "incident": self.memory.incident,

            "timeline": timeline,

            "evidence": evidence,

            "correlations": correlations,

            "graph": {

                "nodes": graph.get("nodes", []),

                "edges": graph.get("edges", [])

            },

            "reasoning": reasoning,

            "root_cause": (
                self.memory.hypotheses[0]
                if self.memory.hypotheses
                else None
            ),

            "recommendations": recommendations,

            "confidence": self.memory.confidence,

            "summary": self.generate_summary(reasoning)

        }

        self.memory.set_final_report(report)

        self.memory.add_timeline_event(
            "Final investigation report generated."
        )

        return report

    def generate_summary(self, reasoning):

        incident = self.memory.incident

        if incident.get("status") == "NO_ISSUE":

            return (
                "No active incident was detected during the investigation."
            )

        severity = incident.get(
            "severity",
            "UNKNOWN"
        )

        title = incident.get(
            "title",
            "Unknown Incident"
        )

        services = reasoning.get("services", {})

        service_list = ", ".join(services.keys())

        if not service_list:
            service_list = "Unknown"

        return (

            f"Investigation completed for '{title}'. "

            f"Severity: {severity}. "

            f"Affected Services: {service_list}. "

            f"Evidence collected: {len(self.memory.evidence)}. "

            f"Recommendations generated: {len(self.memory.recommendations)}. "

            f"Confidence Score: {self.memory.confidence}%."

        )