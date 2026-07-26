from fastapi import APIRouter, Query

from app.coordinator.incident_coordinator import IncidentCoordinator
from app.services.investigation_service import InvestigationService

router = APIRouter(
    prefix="/investigation",
    tags=["Investigation"]
)

coordinator = IncidentCoordinator()

service = InvestigationService()


@router.post("/start")
async def start(service_name: str = Query(default="gateway", min_length=1)):

    result = await coordinator.start_investigation(service_name=service_name)

    return result

@router.get("/history")
def history():

    investigations = service.get_all_investigations()

    return investigations

@router.get("/{investigation_id}")
def get_by_id(investigation_id: int):

    investigation = service.get_investigation_by_id(investigation_id)

    if investigation is None:
        return {
            "status": "NOT_FOUND"
        }

    return investigation

@router.delete("/{investigation_id}")
def delete_investigation(investigation_id: int):

    deleted = service.delete_investigation(investigation_id)

    if not deleted:
        return {
            "status": "NOT_FOUND"
        }

    return {
        "status": "SUCCESS",
        "message": "Investigation deleted successfully."
    }
