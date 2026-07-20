from fastapi import APIRouter

from app.core.settings import settings

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} Backend Running"
    }