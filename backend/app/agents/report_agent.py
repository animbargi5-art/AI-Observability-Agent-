from app.agents.base_agent import BaseAgent


class ReportAgent(BaseAgent):

    def __init__(self, memory):

        super().__init__(
            name="Report Agent",
            description="Generates the final investigation report."
        )

        self.memory = memory

    def execute(self):

        report = {

            "incident": self.memory.incident,

            "timeline": self.memory.timeline,

            "evidence": self.memory.evidence,

            "root_cause": (
                self.memory.hypotheses[0]
                if self.memory.hypotheses
                else None
            ),

            "recommendations": self.memory.recommendations,

            "confidence": self.memory.confidence
        }

        self.memory.set_final_report(report)

        return report