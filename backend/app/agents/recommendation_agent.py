from app.agents.base_agent import BaseAgent
from app.decision.reasoning_engine import ReasoningEngine


class RecommendationAgent(BaseAgent):

    def __init__(self, memory):

        super().__init__(
            name="Recommendation Agent",
            description="Generates recommendations based on investigation evidence."
        )

        self.memory = memory

        self.reasoning_engine = ReasoningEngine(memory)

    def execute(self):

        incident = self.memory.incident
        evidence = self.memory.evidence
        hypotheses = self.memory.hypotheses

        reasoning = self.reasoning_engine.analyze()

        recommendations = []

        # --------------------------------------------------
        # No active incident
        # --------------------------------------------------

        if incident.get("status") == "NO_ISSUE":

            recommendations.append({
                "priority": "LOW",
                "title": "No action required",
                "description": "No active incident was detected."
            })

        # --------------------------------------------------
        # Evidence-based recommendations
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Recommendations from Root Cause Hypotheses
        # --------------------------------------------------

        for hypothesis in hypotheses:

            cause = hypothesis.get("cause", "")

            if "database" in cause.lower():

                recommendations.append({
                    "priority": "HIGH",
                    "title": "Optimize database",
                    "description": (
                        "Investigate slow queries, indexes, "
                        "locks and database performance."
                    )
                })

            elif "service" in cause.lower():

                recommendations.append({
                    "priority": "MEDIUM",
                    "title": "Inspect affected service",
                    "description": (
                        "Review service logs, traces and recent deployments."
                    )
                })

        # --------------------------------------------------
        # Recommendations from Reasoning Engine
        # --------------------------------------------------

        highest = reasoning.get("highest_severity", "NONE")

        if highest == "CRITICAL":

            recommendations.append({
                "priority": "CRITICAL",
                "title": "Immediate investigation required",
                "description": (
                    "Critical evidence detected by the reasoning engine."
                )
            })

        elif highest == "HIGH":

            recommendations.append({
                "priority": "HIGH",
                "title": "Prioritize investigation",
                "description": (
                    "High severity findings should be investigated first."
                )
            })

        # --------------------------------------------------
        # Remove duplicate recommendations
        # --------------------------------------------------

        unique = []

        seen = set()

        for recommendation in recommendations:

            key = recommendation["title"]

            if key not in seen:

                seen.add(key)

                unique.append(recommendation)

        # --------------------------------------------------
        # Save into shared memory
        # --------------------------------------------------

        for recommendation in unique:

            self.memory.add_recommendation(recommendation)

        self.memory.add_timeline_event(
            "Recommendations generated."
        )

        return {

            "total_recommendations": len(unique),

            "recommendations": unique,

            "hypotheses": hypotheses,

            "reasoning": reasoning

        }