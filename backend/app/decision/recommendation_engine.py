"""
===============================================================================
TattvaAI - Recommendation Engine
===============================================================================

Generates actionable recommendations from the identified root causes.

Flow
----
RootCause
        ↓
Recommendation Engine
        ↓
Recommendation
===============================================================================
"""

from __future__ import annotations

from app.models.recommendation import Recommendation
from app.models.root_cause import RootCause
from app.schemas.investigation_state import InvestigationState


class RecommendationEngine:
    """
    Generates remediation recommendations based on AI root cause analysis.
    """

    def execute(
        self,
        state: InvestigationState,
    ) -> InvestigationState:

        recommendations = []

        for root_cause in state.root_causes:

            recommendations.extend(
                self.generate(root_cause)
            )

        state.recommendations = recommendations

        state.timeline.append(
            f"Recommendation Engine generated "
            f"{len(recommendations)} recommendation(s)."
        )

        return state

    # ------------------------------------------------------------------
    # Recommendation Generator
    # ------------------------------------------------------------------

    def generate(
        self,
        root_cause: RootCause,
    ) -> list[Recommendation]:

        probable = root_cause.probable_cause.lower()

        recommendations = []

        # --------------------------------------------------------------
        # Slow API
        # --------------------------------------------------------------

        if "latency" in probable or "slow" in probable:

            recommendations.append(

                Recommendation(

                    service_name=root_cause.service_name,

                    priority="P2",

                    category="Performance",

                    confidence=95,

                    title="Investigate API Latency",

                    description=(
                        "The service is experiencing increased latency."
                    ),

                    action=(
                        "Inspect slow database queries, external API calls, "
                        "CPU utilization and application profiling."
                    ),

                    expected_impact=(
                        "Reduced response time and improved throughput."
                    )

                )

            )

        # --------------------------------------------------------------
        # Application Error
        # --------------------------------------------------------------

        elif "exception" in probable or "application" in probable:

            recommendations.append(

                Recommendation(

                    service_name=root_cause.service_name,

                    priority="P1",

                    category="Application",

                    confidence=98,

                    title="Investigate Application Errors",

                    description=(
                        "Application failures were detected."
                    ),

                    action=(
                        "Review stack traces, application logs and "
                        "recent deployments."
                    ),

                    expected_impact=(
                        "Restore application stability."
                    )

                )

            )

        # --------------------------------------------------------------
        # Dependency Failure
        # --------------------------------------------------------------

        elif "dependency" in probable:

            recommendations.append(

                Recommendation(

                    service_name=root_cause.service_name,

                    priority="P1",

                    category="Infrastructure",

                    confidence=96,

                    title="Inspect Downstream Dependency",

                    description=(
                        "A downstream dependency appears unhealthy."
                    ),

                    action=(
                        "Verify dependency health, retry policies, "
                        "network latency and timeout settings."
                    ),

                    expected_impact=(
                        "Improve service reliability."
                    )

                )

            )

        # --------------------------------------------------------------
        # Traffic
        # --------------------------------------------------------------

        elif "traffic" in probable:

            recommendations.append(

                Recommendation(

                    service_name=root_cause.service_name,

                    priority="P2",

                    category="Infrastructure",

                    confidence=90,

                    title="Scale Service",

                    description=(
                        "Traffic volume has increased significantly."
                    ),

                    action=(
                        "Scale application replicas or enable autoscaling."
                    ),

                    expected_impact=(
                        "Reduce request queue time."
                    )

                )

            )

        # --------------------------------------------------------------
        # Default
        # --------------------------------------------------------------

        else:

            recommendations.append(

                Recommendation(

                    service_name=root_cause.service_name,

                    priority="P3",

                    category="General",

                    confidence=70,

                    title="Continue Investigation",

                    description=(
                        "No specific remediation was identified."
                    ),

                    action=(
                        "Review telemetry, logs and infrastructure."
                    ),

                    expected_impact=(
                        "Additional evidence may reveal the root cause."
                    )

                )

            )

        return recommendations