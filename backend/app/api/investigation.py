from fastapi import APIRouter

from app.coordinator.incident_coordinator import IncidentCoordinator

router = APIRouter(
    prefix="/investigation",
    tags=["Investigation"]
)

coordinator = IncidentCoordinator()


@router.post("/start")
def start():

    result = coordinator.start_investigation()

    return result