from app.agents.base_agent import BaseAgent
from app.tools.dependency_tool import DependencyTool
from app.memory.investigation_memory import InvestigationMemory


class DependencyAgent(BaseAgent):

    def __init__(self, memory=None):

        super().__init__(
            "Dependency Agent",
            "Analyzes service dependencies from SigNoz."
        )

        self.dependency_tool = DependencyTool()

        if memory is None:
            self.memory = InvestigationMemory()

        else:
            self.memory = memory

    def fetch_dependencies(self):
        return self.dependency_tool.execute()

    def execute(self):

        result = self.fetch_dependencies()

        dependencies = result.get("dependencies", [])

        findings = []

        for dependency in dependencies:

            findings.append({
                "source": dependency.get("source"),
                "target": dependency.get("target"),
                "latency_ms": dependency.get("latency_ms", 0),
                "error_rate": dependency.get("error_rate", 0)
            })

        # Store findings in Shared Investigation Memory
        for finding in findings:
            self.memory.add_evidence(finding)

        # Record investigation progress
        self.memory.add_timeline_event(
            "Dependency investigation completed."
        )

        # Temporary confidence score
        if findings:
            self.memory.set_confidence(80)

        return {
            "total_dependencies": len(findings),
            "findings": findings
        }