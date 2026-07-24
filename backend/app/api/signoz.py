from fastapi import APIRouter

router = APIRouter(
    prefix="/signoz",
    tags=["SigNoz"],
)

from app.services.signoz import SigNozService

service = SigNozService()

@router.get("/metrics")
async def list_metrics():

    await service.connect()

    try:

        result = await service.list_metrics()

        return result

    finally:

        await service.disconnect()