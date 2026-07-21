from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.root import router as root_router
from app.api.investigation import router as investigation_router
from app.api.demo import router as demo_router

from app.telemetry.tracing import setup_tracing
from app.core.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Evidence-Driven Incident Intelligence",
    version=settings.APP_VERSION,
)

app.include_router(root_router)
app.include_router(health_router)
app.include_router(investigation_router)
app.include_router(demo_router)

setup_tracing(app)