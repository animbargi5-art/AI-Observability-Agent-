from app.memory.manager import InvestigationMemory

from app.graph.workflow import graph


class IncidentCoordinator:

    def __init__(self):

        self.memory = InvestigationMemory()

    def start_investigation(
        self,
        incident_id: str,
        service_name: str
    ):

        investigation = self.memory.create(
            incident_id,
            service_name,
        )

        result = graph.invoke(
            {

                "investigation": investigation,

                "traces": [],

                 "logs": [],

        "metrics": [],

        "dependencies": [],

        "historical_incidents": [],

        "evidence": [],

        "hypotheses": [],

        "recommendations": []
    }
)

        return result