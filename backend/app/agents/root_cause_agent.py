from app.agents.base_agent import BaseAgent
from app.memory.investigation_memory import InvestigationMemory


class RootCauseAgent(BaseAgent):

    def __init__(self, memory: InvestigationMemory):

        super().__init__(
            name="Root Cause Agent",
            description="Analyzes all collected evidence to determine the most probable root cause."
        )

        self.memory = memory

    def execute(self):

        evidence = self.memory.evidence

        print(f"Collected Evidence: {len(evidence)}")

        if len(evidence) == 0:

            hypothesis = {
                "cause": "No evidence available",
                "confidence": 0
            }

            self.memory.add_hypothesis(hypothesis)

            self.memory.set_confidence(0)

            return {
                "root_cause": None,
                "confidence": 0
            }

        services = {}

        for item in evidence:

            service = (
                item.get("trace", {})
                    .get("service", "Unknown Service")
            )

            services[service] = services.get(service, 0) + 1

        most_likely = max(
            services,
            key=services.get
        )

        hypothesis = {
            "cause": f"Most evidence points to {most_likely}",
            "confidence": 70
        }

        self.memory.add_hypothesis(hypothesis)

        self.memory.set_confidence(70)

        return {
            "root_cause": hypothesis["cause"],
            "confidence": 70
        }