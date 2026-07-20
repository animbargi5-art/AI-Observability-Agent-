from app.agents.base_agent import BaseAgent

class RecommendationAgent(BaseAgent):

    def __init__(self, memory):

        super().__init__(
            name="Recommendation Agent",
            description="Generates recommendations based on investigation evidence."
        )

        self.memory = memory

    def execute(self):

        incident = self.memory.incident
        evidence = self.memory.evidence
        hypotheses = self.memory.hypotheses

        recommendations = []

        if incident.get("status") == "NO_ISSUE":

            recommendations.append({
                "priority": "LOW",
                "title": "No action required",
                "description": "No active incident was detected."
            })

        for item in evidence:

            incident_type = item.get("type", "")

            if incident_type == "Slow API":

                recommendations.append({
                    "priority": "HIGH",
                    "title": "Investigate database performance",
                    "description": (
                        "Check slow SQL queries, database indexes "
                        "and connection pool usage."
                    )
                })

            elif incident_type == "Server Error":

                recommendations.append({
                    "priority": "CRITICAL",
                    "title": "Inspect application errors",
                    "description": (
                        "Review stack traces and recent deployments."
                    )
                })

            elif incident_type == "Client Error":

                recommendations.append({
                    "priority": "MEDIUM",
                    "title": "Review client requests",
                    "description": (
                        "Validate request payloads and API contracts."
                    )
                })

        for recommendation in recommendations:
            self.memory.add_recommendation(recommendation)

        return {
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "hypotheses": hypotheses
        }