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

    async def execute(self):

        incident = self.memory.incident
        evidence = self.memory.evidence
        hypotheses = self.memory.hypotheses

        reasoning = self.reasoning_engine.analyze()

        highest_severity = reasoning["highest_severity"]

        confidence = self.memory.confidence

        suspicious_services = reasoning["suspicious_services"]

        recommendations = []

        # --------------------------------------------------
        # No active incident
        # --------------------------------------------------

        if incident.get("status") == "NO_ISSUE":

            recommendations.append({
                "priority": "LOW",
                "title": "No Action Required",
                "description": "No active incident was detected."
            })

        # --------------------------------------------------
        # Evidence-based recommendations
        # --------------------------------------------------

        for item in evidence:

            incident_type = item.get("type", "")

            # ----------------------------------------------
            # Slow APIs
            # ----------------------------------------------

            if incident_type in ["Slow API", "Critical Slow API"]:

                recommendations.append({
                    "priority": (
                        "CRITICAL"
                        if incident_type == "Critical Slow API"
                        else "HIGH"
                    ),
                    "title": "Investigate API Latency",
                    "description": (
                        "Profile the endpoint, inspect SQL queries, "
                        "review external dependencies, thread blocking, "
                        "and database connection pool usage."
                    )
                })

            # ----------------------------------------------
            # Application / Server Errors
            # ----------------------------------------------

            elif incident_type in ["Server Error", "Application Error"]:

                recommendations.append({
                    "priority": "CRITICAL",
                    "title": "Inspect Application Errors",
                    "description": (
                        "Review stack traces, exception logs, "
                        "and application telemetry."
                    )
                })

                recommendations.append({
                    "priority": "HIGH",
                    "title": "Review Recent Deployment",
                    "description": (
                        "Compare the latest deployment with the previous release, "
                        "inspect configuration changes and recent commits."
                    )
                })

            # ----------------------------------------------
            # Client Errors
            # ----------------------------------------------

            elif incident_type == "Client Error":

                recommendations.append({
                    "priority": "MEDIUM",
                    "title": "Review Client Requests",
                    "description": (
                        "Validate request payloads, authentication, "
                        "and API contracts."
                    )
                })

            # ----------------------------------------------
            # Traffic Spikes
            # ----------------------------------------------

            elif incident_type == "Traffic Spike":

                recommendations.append({
                    "priority": "MEDIUM",
                    "title": "Investigate Traffic Surge",
                    "description": (
                        "Verify autoscaling, inspect request patterns, "
                        "review load balancer metrics and identify abnormal traffic."
                    )
                })

        # --------------------------------------------------
        # Recommendations from Root Cause Hypotheses
        # --------------------------------------------------

        for hypothesis in hypotheses:

            cause = hypothesis.get("cause", "").lower()

            if "database" in cause:

                recommendations.append({
                    "priority": "HIGH",
                    "title": "Optimize Database",
                    "description": (
                        "Investigate slow queries, indexes, locks, "
                        "connection pools and overall database performance."
                    )
                })

            elif "latency" in cause:

                recommendations.append({
                    "priority": "HIGH",
                    "title": "Investigate Service Latency",
                    "description": (
                        "Analyze endpoint latency, downstream dependencies "
                        "and infrastructure bottlenecks."
                    )
                })

            elif "application" in cause:

                recommendations.append({
                    "priority": "HIGH",
                    "title": "Resolve Application Exceptions",
                    "description": (
                        "Inspect application logs, exception traces "
                        "and recent code changes."
                    )
                })

            elif "traffic" in cause:

                recommendations.append({
                    "priority": "MEDIUM",
                    "title": "Manage Traffic Growth",
                    "description": (
                        "Review scaling policies, rate limiting "
                        "and traffic distribution."
                    )
                })

            elif "service" in cause:

                recommendations.append({
                    "priority": "MEDIUM",
                    "title": "Inspect Affected Service",
                    "description": (
                        "Review service logs, distributed traces "
                        "and recent deployments."
                    )
                })

        # --------------------------------------------------
        # Recommendations from Reasoning Engine
        # --------------------------------------------------

        if highest_severity == "CRITICAL":

            recommendations.append({
                "priority": "CRITICAL",
                "title": "Immediate Investigation Required",
                "description":
                    "Critical services were detected. Escalate immediately."
            })

        elif highest_severity == "HIGH":

            recommendations.append({
                "priority": "HIGH",
                "title": "Prioritize Investigation",
                "description":
                    "High severity findings should be investigated first."
            })

        elif highest_severity == "MEDIUM":

            recommendations.append({
                "priority": "MEDIUM",
                "title": "Continue Active Monitoring",
                "description":
                    "Continue monitoring while investigating affected services."
            })

        elif highest_severity == "LOW":

            recommendations.append({
                "priority": "LOW",
                "title": "Monitor Performance",
                "description":
                    "Continue monitoring application latency. No immediate action is required."
            })

        # --------------------------------------------------
        # Confidence-based recommendations
        # --------------------------------------------------

        if confidence >= 80:

            recommendations.append({
                "priority": "HIGH",
                "title": "High Confidence Root Cause",
                "description":
                    "The investigation produced a high-confidence root cause. Verify and begin remediation."
            })

        elif confidence >= 50:

            recommendations.append({
                "priority": "MEDIUM",
                "title": "Validate Root Cause",
                "description":
                    "Verify the suspected root cause using additional traces, logs and metrics."
            })

        else:

            recommendations.append({
                "priority": "LOW",
                "title": "Collect More Evidence",
                "description":
                    "Investigation confidence is low. Gather additional traces, metrics and logs."
            })

        # --------------------------------------------------
        # Suspicious Services
        # --------------------------------------------------

        service_names = sorted({
            item.get("service", "Unknown")
            for item in suspicious_services
        })

        if service_names:

            recommendations.append({
                "priority": "HIGH",
                "title": "Investigate Suspicious Services",
                "description":
                    f"Review these services: {', '.join(service_names)}"
            })

        # --------------------------------------------------
        # Remove duplicate recommendations
        # --------------------------------------------------

        unique = []

        seen = set()

        for recommendation in recommendations:

            if recommendation["title"] not in seen:

                seen.add(recommendation["title"])

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