"""
===============================================================================
TattvaAI - Application Telemetry Service
===============================================================================

Purpose
-------
Converts raw SigNoz telemetry into normalized domain models.

Responsibilities
----------------
• Retrieve telemetry from SigNoz
• Parse raw MCP responses
• Convert into domain models
• Hide SigNoz response structure from the Tool layer

Architecture
------------
Tools
    ↓
Application Telemetry Service
    ↓
SigNoz Telemetry Service
    ↓
MCP Gateway
    ↓
SigNoz

===============================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from mcp.types import TextContent

from app.core.logger import logger

from app.models.trace import Trace
from app.models.log import Log
from app.models.metric import Metric
from app.models.dependency import Dependency
from app.models.alert import Alert

from app.signoz.telemetry_service import (
    TelemetryService as SigNozTelemetryService,
)


class TelemetryService:
    """
    Application telemetry service.

    Converts raw SigNoz responses into normalized domain objects.
    """

    def __init__(self):

        self.signoz = SigNozTelemetryService()

    # =====================================================================
    # Helpers
    # =====================================================================

    def _extract_payload(self, result: Any) -> dict:

        if result is None:
            return {}

        if isinstance(result, dict):
            return result

        if hasattr(result, "content"):

            for item in result.content:

                if isinstance(item, TextContent):

                    try:
                        return json.loads(item.text)

                    except Exception:

                        logger.exception(
                            "Unable to parse MCP response."
                        )

        return {}

    # =====================================================================
    # Trace Conversion
    # =====================================================================

    async def get_traces(
        self,
        service_name: str,
        **kwargs,
    ) -> list[Trace]:

        raw = await self.signoz.search_traces(
            service_name,
            **kwargs,
        )

        payload = self._extract_payload(raw)

        rows = (
            payload.get("data", {})
            .get("data", {})
            .get("results", [{}])[0]
            .get("rows", [])
        )

        traces: list[Trace] = []

        for row in rows:

            data = row.get("data", {})

            traces.append(

                Trace(

                    trace_id=data.get("trace_id", ""),

                    span_id=data.get("span_id"),

                    service_name=data.get(
                        "service.name",
                        "Unknown",
                    ),

                    operation_name=data.get(
                        "name",
                        "",
                    ),

                    endpoint=data.get(
                        "name",
                        "",
                    ),

                    http_method=(
                        data.get("http_method")
                        or data.get(
                            "http.request.method"
                        )
                    ),

                    duration_ms=round(
                        data.get(
                            "duration_nano",
                            0,
                        )
                        / 1_000_000,
                        2,
                    ),

                    status_code=(
                        int(
                            data.get(
                                "response_status_code",
                                0,
                            )
                        )
                        if data.get(
                            "response_status_code"
                        )
                        else None
                    ),

                    status=str(
                        data.get(
                            "response_status_code",
                            "",
                        )
                    ),

                    timestamp=datetime.utcnow(),

                )

            )

        logger.info(
            "Loaded %d traces",
            len(traces),
        )

        return traces

    # =====================================================================
    # Logs
    # =====================================================================

    async def get_logs(
        self,
        service_name: str,
        **kwargs,
    ) -> list[Log]:

        raw = await self.signoz.search_logs(
            service_name,
            **kwargs,
        )

        payload = self._extract_payload(raw)

        rows = (
            payload.get("data", {})
            .get("data", {})
            .get("results", [{}])[0]
            .get("rows", [])
        )

        logs: list[Log] = []

        for row in rows:

            data = row.get("data", {})

            logs.append(

                Log(

                    log_id=data.get("id"),

                    trace_id=data.get("trace_id"),

                    span_id=data.get("span_id"),

                    service_name=(
                        data.get(
                            "resources_string",
                            {},
                        ).get(
                            "service.name",
                            "Unknown",
                        )
                    ),

                    severity=data.get(
                        "severity_text",
                        "INFO",
                    ),

                    message=data.get(
                        "body",
                        "",
                    ),

                    timestamp=datetime.utcnow(),

                )

            )

        logger.info(
            "Loaded %d logs",
            len(logs),
        )

        return logs

    # =====================================================================
    # Metrics
    # =====================================================================

    async def get_metrics(
        self,
        service_name: str,
        metric_name: str,
        **kwargs,
    ) -> list[Metric]:

        raw = await self.signoz.query_metrics(
            service_name,
            metric_name,
            **kwargs,
        )

        payload = self._extract_payload(raw)

        results = (
            payload.get("data", {})
            .get("data", {})
            .get("results", [])
        )

        metrics: list[Metric] = []

        if not results:
            return metrics

        aggregations = results[0].get(
            "aggregations",
            [],
        )

        if not aggregations:
            return metrics

        series = aggregations[0].get(
            "series",
            [],
        )

        if not series:
            return metrics

        for point in series[0].get(
            "values",
            [],
        ):

            metrics.append(

                Metric(

                    metric_name=metric_name,

                    service_name=service_name,

                    value=point.get(
                        "value",
                        0,
                    ),

                    timestamp=datetime.utcnow(),

                )

            )

        logger.info(
            "Loaded %d metrics",
            len(metrics),
        )

        return metrics

    # =====================================================================
    # Dependencies
    # =====================================================================

    async def get_dependencies(
        self,
        service_name: str,
        **kwargs,
    ) -> list[Dependency]:

        raw = await self.signoz.get_dependencies(
            service_name,
            **kwargs,
        )

        payload = self._extract_payload(raw)

        rows = payload.get(
            "dependencies",
            [],
        )

        dependencies: list[
            Dependency
        ] = []

        for item in rows:

            dependencies.append(

                Dependency(

                    source_service=item.get(
                        "source",
                        "",
                    ),

                    target_service=item.get(
                        "target",
                        "",
                    ),

                    average_latency_ms=item.get(
                        "latency_ms",
                        0,
                    ),

                    error_rate=item.get(
                        "error_rate",
                        0,
                    ),

                )

            )

        logger.info(
            "Loaded %d dependencies",
            len(dependencies),
        )

        return dependencies

    # =====================================================================
    # Alerts
    # =====================================================================

    async def get_alerts(self) -> list[Alert]:

        raw = await self.signoz.gateway.list_alerts()

        payload = self._extract_payload(raw)

        alerts: list[Alert] = []

        for item in payload.get(
            "alerts",
            [],
        ):

            alerts.append(

                Alert(

                    alert_id=item.get(
                        "id",
                        "",
                    ),

                    name=item.get(
                        "name",
                        "",
                    ),

                    service_name=item.get(
                        "service",
                        "Unknown",
                    ),

                    severity=item.get(
                        "severity",
                        "LOW",
                    ),

                    status=item.get(
                        "status",
                        "UNKNOWN",
                    ),

                )

            )

        logger.info(
            "Loaded %d alerts",
            len(alerts),
        )

        return alerts