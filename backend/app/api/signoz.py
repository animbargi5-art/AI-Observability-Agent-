from fastapi import APIRouter

router = APIRouter(
    prefix="/signoz",
    tags=["SigNoz"],
)

from app.signoz.telemetry_service import TelemetryService

service = TelemetryService()

@router.get("/metrics")
async def list_metrics():

    return await service.list_metrics()
