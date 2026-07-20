from fastapi import APIRouter

from app.agents.coordinator import IncidentCoordinator

router = APIRouter()

coordinator = IncidentCoordinator()


@router.post("/investigation/start")
def start():

    state = coordinator.start_investigation(
        incident_id="INC-001",
        service_name="payment-service"
    )

    return state