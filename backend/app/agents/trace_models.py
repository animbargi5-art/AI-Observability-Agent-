from pydantic import BaseModel


class TraceSummary(BaseModel):
    service_name: str
    endpoint: str
    duration_ms: float
    status_code: int | None
    timestamp: str