from pydantic import BaseModel, Field
from typing import List, Dict


class InvestigationState(BaseModel):
    """
    Shared investigation state used by all AI agents.
    """

    incident_id: str

    service_name: str

    investigation_status: str = "running"

    traces: List[Dict] = Field(default_factory=list)

    logs: List[Dict] = Field(default_factory=list)

    metrics: List[Dict] = Field(default_factory=list)

    dependencies: List[Dict] = Field(default_factory=list)

    historical_incidents: List[Dict] = Field(default_factory=list)

    evidence: List[Dict] = Field(default_factory=list)

    hypotheses: List[str] = Field(default_factory=list)

    recommendations: List[str] = Field(default_factory=list)

    confidence_score: float = 0.0