from app.memory.manager import InvestigationMemory


class IncidentCoordinator:

    def __init__(self):

        self.memory = InvestigationMemory()

    def start_investigation(
        self,
        incident_id: str,
        service_name: str
    ):

        return self.memory.create(
            incident_id,
            service_name
        )