from fastapi import APIRouter
import time

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }

@router.get("/test")
def test():
    time.sleep(2)
    return {
        "status": "ok",
        "message": "Telemetry Test"
    }