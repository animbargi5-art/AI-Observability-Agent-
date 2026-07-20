from app.schemas.investigation import InvestigationState


class InvestigationMemory:

    def __init__(self):
        self.current_state = None

    def create(self, incident_id: str, service_name: str):

        self.current_state = InvestigationState(
            incident_id=incident_id,
            service_name=service_name
        )

        return self.current_state

    def get(self):

        return self.current_state