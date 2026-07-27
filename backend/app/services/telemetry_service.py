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
from pathlib import Path

from datetime import datetime
from typing import Any

from mcp.types import TextContent

from app.core.logger import logger

from app.models.trace import Trace
from app.models.log import Log
from app.models.metric import Metric
from app.models.dependency import Dependency
from app.models.alert import Alert
from app.models.historical_incident import HistoricalIncident

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

    def _extract_payload(self, raw) -> dict:

        # MCPGateway already converts CallToolResult text into native Python
        # data.  Keep accepting the original result shape for compatibility,
        # but do not discard the live SigNoz response once it is a dict.
        if isinstance(raw, dict):
            return raw

        if isinstance(raw, str):
            try:
                payload = json.loads(raw)
                return payload if isinstance(payload, dict) else {}
            except json.JSONDecodeError:
                return {}

        logger.info("=" * 80)
        logger.info("RAW MCP RESPONSE")
        logger.info("=" * 80)

        logger.info("TYPE: %s", type(raw))
        logger.info("RAW OBJECT:\n%s", raw)

        if hasattr(raw, "content"):

            logger.info(
                "CONTENT COUNT: %d",
                len(raw.content),
            )

            for i, item in enumerate(raw.content):

                logger.info("-" * 60)
                logger.info("Item %d", i)
                logger.info("TYPE: %s", type(item))

                if hasattr(item, "text"):

                    logger.info("TEXT:")
                    logger.info(repr(item.text))

                if isinstance(item, TextContent):

                    try:

                        Path("payload.json").write_text(
                            item.text,
                            encoding="utf-8",
                        )

                        return json.loads(item.text)

                    except Exception:

                        logger.exception(
                            "Unable to parse MCP response."
                        )

        logger.info("=" * 80)
        logger.info("No JSON payload found.")
        logger.info("=" * 80)

        return {}

    # =====================================================================
    # Trace Conversion
    # =====================================================================

    async def get_traces(
        self,
        service_name: str,
        **kwargs,
    ) -> list[Trace]:

        # Demo mode: return mock traces
        from app.core.settings import settings
        if settings.DEMO_MODE:
            return self._generate_mock_traces(service_name)

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

        # Demo mode: return mock logs
        from app.core.settings import settings
        if settings.DEMO_MODE:
            return self._generate_mock_logs(service_name)

        raw = await self.signoz.search_logs(
            service_name,
            **kwargs,
        )

        payload = self._extract_payload(raw)


        logger.info(
            json.dumps(
                payload,
                indent=2,
                default=str,
            )
        )

        results = (
            payload.get("data", {})
            .get("data", {})
            .get("results")
        )

        rows = results[0].get("rows", []) if results else []

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

        # Demo mode: return mock metrics
        from app.core.settings import settings
        if settings.DEMO_MODE:
            return self._generate_mock_metrics(service_name, metric_name)

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

        # Demo mode: return mock dependencies
        from app.core.settings import settings
        if settings.DEMO_MODE:
            return self._generate_mock_dependencies(service_name)

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

        # Demo mode: return mock alerts
        from app.core.settings import settings
        if settings.DEMO_MODE:
            return self._generate_mock_alerts("gateway")

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

    # -------------------------------------------------------------------------
    # Historical Incidents
    # -------------------------------------------------------------------------

    async def get_historical_incidents(
        self,
        service_name: str,
        **kwargs,
    ) -> list[HistoricalIncident]:
        """
        Retrieve historical incidents for the specified service.
        Convert from SigNoz telemetry data into HistoricalIncident models.
        """
        logger.info("Getting historical incidents for service: %s", service_name)

        from app.core.settings import settings

        if settings.DEMO_MODE:
            return self._generate_mock_historical_incidents(service_name)

        # Use the new method that returns proper HistoricalIncident models
        incidents = await self.signoz.get_historical_incidents_as_models(
            service_name=service_name,
            **kwargs,
        )
        
        logger.info("Retrieved %d historical incidents", len(incidents))
        return incidents

    async def health_check(self) -> bool:
        """
        Check telemetry service health.
        """
        return await self.signoz.health_check()
    # =====================================================================
    # Demo Mode Mock Data Generation
    # =====================================================================

    def _generate_mock_traces(self, service_name: str) -> list[Trace]:
        """Generate mock trace data for demo mode."""
        from datetime import datetime, timedelta
        
        traces = []
        for i in range(5):
            trace = Trace(
                trace_id=f"trace_{service_name}_{i}",
                span_id=f"span_{service_name}_{i}",
                operation_name=f"/{service_name}/api/endpoint",
                service_name=service_name,
                duration_ms=100 + (i * 50),
                timestamp=datetime.now() - timedelta(minutes=i * 5),
                status_code=500 if i == 2 else 200,  # Use integer status codes
                status="ERROR" if i == 2 else "OK",
                error_message="Database connection timeout" if i == 2 else None,
                attributes={"http.method": "GET", "http.url": f"/{service_name}/api"}
            )
            traces.append(trace)
        return traces

    def _generate_mock_logs(self, service_name: str) -> list[Log]:
        """Generate mock log data for demo mode."""
        from datetime import datetime, timedelta
        
        logs = []
        for i in range(5):
            log = Log(
                timestamp=datetime.now() - timedelta(minutes=i * 5),
                severity="ERROR" if i == 2 else "INFO",
                message=f"Connection timeout to database" if i == 2 else f"Processing request {i}",
                service_name=service_name,
                trace_id=f"trace_{service_name}_{i}",
                span_id=f"span_{service_name}_{i}",
                attributes={"component": service_name},
                exception_message="Connection refused" if i == 2 else None
            )
            logs.append(log)
        return logs

    def _generate_mock_metrics(self, service_name: str, metric_name: str = "response_time") -> list[Metric]:
        """Generate mock metric data for demo mode."""
        from datetime import datetime, timedelta
        
        metrics = []
        for i in range(5):
            metric = Metric(
                metric_name=metric_name,
                value=50.0 + (i * 10) if metric_name == "response_time" else 0.95 - (i * 0.1),
                timestamp=datetime.now() - timedelta(minutes=i * 5),
                service_name=service_name,
                labels={"endpoint": "/api/health"},
                unit="ms" if metric_name == "response_time" else "percent"
            )
            metrics.append(metric)
        return metrics

    def _generate_mock_dependencies(self, service_name: str) -> list[Dependency]:
        """Generate mock dependency data for demo mode."""
        dependencies = []
        if service_name == "gateway":
            deps_data = [
                {"target": "inventory", "call_rate": 150.0, "error_rate": 0.02},
                {"target": "order", "call_rate": 100.0, "error_rate": 0.01},
                {"target": "payment", "call_rate": 80.0, "error_rate": 0.05}
            ]
        else:
            deps_data = [{"target": "database", "call_rate": 200.0, "error_rate": 0.01}]
            
        for dep_data in deps_data:
            dependency = Dependency(
                source_service=service_name,
                target_service=dep_data["target"],
                operation="HTTP",
                call_rate=dep_data["call_rate"],
                error_rate=dep_data["error_rate"],
                p99_latency=100.0,
                dependency_type="HTTP"
            )
            dependencies.append(dependency)
        return dependencies

    def _generate_mock_alerts(self, service_name: str) -> list[Alert]:
        """Generate mock alert data for demo mode."""
        from datetime import datetime, timedelta
        
        alerts = []
        alert = Alert(
            alert_id=f"alert_{service_name}_1",
            name="High Error Rate",
            severity="HIGH",
            status="FIRING",
            service_name=service_name,
            description=f"Error rate above threshold for {service_name}",
            fired_at=datetime.now() - timedelta(minutes=30),
            last_updated=datetime.now() - timedelta(minutes=5),
            labels={"alertname": "HighErrorRate", "service": service_name}
        )
        alerts.append(alert)
        return alerts

    def _generate_mock_historical_incidents(self, service_name: str) -> list[HistoricalIncident]:
        """Generate mock historical incident data for demo mode."""
        from datetime import datetime, timedelta
        
        resolved_at = datetime.now() - timedelta(days=7)
        return [
            HistoricalIncident(
                incident_id=f"incident_{service_name}_1",
                title=f"Database connection timeout in {service_name}",
                service_name=service_name,
                endpoint="/api/checkout",
                operation="POST /api/checkout",
                environment="demo",
                severity="HIGH",
                status="RESOLVED",
                root_cause="Database connection pool exhaustion",
                resolution="Increased connection pool size and added connection retry logic",
                confidence=94,
                similarity_score=0.94,
                occurrence_count=3,
                resolved_by="TattvaAI demo",
                previous_recommendation="Scale the connection pool and add retry telemetry.",
                started_at=resolved_at - timedelta(hours=2),
                resolved_at=resolved_at,
                tags=[service_name, "database", "performance"],
                metadata={"scenario": "demo"},
            )
        ]
