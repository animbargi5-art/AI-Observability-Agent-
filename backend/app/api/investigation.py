from fastapi import APIRouter, Query

from app.coordinator.incident_coordinator import IncidentCoordinator
from app.services.investigation_store import investigation_store

router = APIRouter(
    prefix="/investigation",
    tags=["Investigation"]
)

coordinator = IncidentCoordinator()

@router.post("/start")
async def start(service_name: str = Query(default="gateway", min_length=1)):

    result = await coordinator.start_investigation(service_name=service_name)
    return investigation_store.save(result)

@router.get("/history")
def history():
    return investigation_store.list()

@router.get("/{investigation_id}")
def get_by_id(investigation_id: str):

    investigation = investigation_store.get(investigation_id)

    if investigation is None:
        return {
            "status": "NOT_FOUND"
        }

    return investigation

@router.delete("/{investigation_id}")
def delete_investigation(investigation_id: str):

    deleted = investigation_store.delete(investigation_id)

    if not deleted:
        return {
            "status": "NOT_FOUND"
        }

    return {
        "status": "SUCCESS",
        "message": "Investigation deleted successfully."
    }
