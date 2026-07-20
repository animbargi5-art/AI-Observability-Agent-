from typing import TypedDict

from app.schemas.investigation import InvestigationState


class GraphState(TypedDict):
    """
    Shared LangGraph state.

    Every agent writes only to its own section.
    """

    investigation: InvestigationState

    traces: list

    logs: list

    metrics: list

    dependencies: list

    historical_incidents: list

    evidence: list

    hypotheses: list

    recommendations: list