from app.agents.base_agent import BaseAgent
from app.tools.dependency_tool import DependencyTool
from app.memory.investigation_memory import InvestigationMemory


class DependencyAgent(BaseAgent):
    """
    Collects service dependency information and stores it
    inside the shared investigation memory.
    """

    def __init__(self, memory=None):

        super().__init__(
            name="Dependency Agent",
            description="Analyzes service dependencies from SigNoz."
        )

        self.dependency_tool = DependencyTool()

        if memory is None:
            self.memory = InvestigationMemory()
        else:
            self.memory = memory

    async def fetch_dependencies(self):

        return await self.dependency_tool.execute()

    async def execute(self):

        result = await self.fetch_dependencies()

        dependencies = result.get("dependencies", [])

        print("\n========== DEPENDENCY AGENT ==========")
        print(f"Dependencies Found: {len(dependencies)}")
        print("======================================\n")

        findings = []

        for dependency in dependencies:

            finding = {

                "severity": "LOW",

                "confidence": 70,

                "category": "Infrastructure",

                "type": "Service Dependency",

                "root_service": dependency.get("source"),

                "source": dependency.get("source"),

                "target": dependency.get("target"),

                "latency_ms": dependency.get(
                    "latency_ms",
                    0
                ),

                "error_rate": dependency.get(
                    "error_rate",
                    0
                )

            }

            findings.append(finding)

        # ---------------------------------------------
        # Save evidence
        # ---------------------------------------------

        for finding in findings:

            self.memory.add_evidence(finding)

        # ---------------------------------------------
        # Timeline
        # ---------------------------------------------

        self.memory.add_timeline_event(
            "Dependency analysis completed."
        )

        # ---------------------------------------------
        # Confidence
        # ---------------------------------------------

        if findings:

            highest = max(
                finding["confidence"]
                for finding in findings
            )

            self.memory.set_confidence(highest)

        print(
            f"Dependency Findings Stored: {len(findings)}"
        )

        return {

            "total_dependencies": len(findings),

            "findings": findings

        }