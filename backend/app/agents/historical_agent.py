from app.agents.base_agent import BaseAgent
from app.tools.historical_tool import HistoricalTool
from app.memory.investigation_memory import InvestigationMemory


class HistoricalAgent(BaseAgent):

    def __init__(self, memory=None):

        super().__init__(
            "Historical Agent",
            "Searches previous investigations for similar incidents."
        )

        self.history_tool = HistoricalTool()

        if memory is None:
            self.memory = InvestigationMemory()
        else:
            self.memory = memory

    async def execute(self):

        history = await self.history_tool.execute()

        findings = []

        for incident in history["history"]:
            findings.append(incident)

        # Store evidence
        for finding in findings:
            self.memory.add_evidence(finding)

        # Timeline
        self.memory.add_timeline_event(
            "Historical investigation completed."
        )

        # Temporary confidence
        if findings:
            self.memory.set_confidence(75)

        return {
            "total_history": len(findings),
            "findings": findings
        }