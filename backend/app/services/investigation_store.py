"""Small in-memory store for completed investigations in the local demo stack."""

from __future__ import annotations

from collections import OrderedDict
from datetime import datetime, timezone
from typing import Any


class InvestigationStore:
    def __init__(self) -> None:
        self._items: OrderedDict[str, dict[str, Any]] = OrderedDict()

    def save(self, result: dict[str, Any] | Any) -> dict[str, Any]:
        if hasattr(result, "model_dump"):
            result = result.model_dump()
        elif not isinstance(result, dict):
            result = dict(result)

        investigation_id = str(result.get("investigation_id") or result.get("incident_id"))
        report = result.get("final_report") or {}
        if hasattr(report, "model_dump"):
            report = report.model_dump()
        report_status = report.get("status")
        report_status = getattr(report_status, "value", report_status)
        report_status = str(report_status).upper() if report_status else None
        item = {
            **result,
            "investigation_id": investigation_id,
            "incident_id": result.get("incident_id", investigation_id),
            "title": report.get("title") or f"Investigation for {result.get('service_name', 'service')}",
            "status": "COMPLETED" if report_status in (None, "", "UNKNOWN") else report_status,
            "severity": report.get("severity") or "LOW",
            "confidence": result.get("confidence", report.get("confidence", 0)),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._items[investigation_id] = item
        self._items.move_to_end(investigation_id)
        while len(self._items) > 50:
            self._items.popitem(last=False)
        return item

    def get(self, investigation_id: str) -> dict[str, Any] | None:
        return self._items.get(str(investigation_id))

    def list(self, limit: int | None = None) -> list[dict[str, Any]]:
        items = list(reversed(self._items.values()))
        return items if limit is None else items[:limit]

    def delete(self, investigation_id: str) -> bool:
        return self._items.pop(str(investigation_id), None) is not None


investigation_store = InvestigationStore()
