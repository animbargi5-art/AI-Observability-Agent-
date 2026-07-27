"""
===============================================================================
TattvaAI - SigNoz Telemetry Service
===============================================================================

Purpose
-------
Provides a high-level interface for retrieving telemetry data from SigNoz.

Responsibilities
----------------
• Search traces
• Retrieve trace details
• Search logs
• Query metrics
• Retrieve dependencies
• Retrieve services
• Execute Query Builder requests

This service hides the MCP Gateway from the application layer.

Architecture
------------
Application Service
        ↓
SigNoz Telemetry Service
        ↓
Query Builder
        ↓
MCP Gateway
        ↓
SigNoz MCP Server
===============================================================================
"""

from __future__ import annotations

import json

from datetime import datetime
from typing import Any
from mcp.types import TextContent
from app.core.logger import logger
from app.signoz.mcp_gateway import MCPGateway
from app.signoz.query_builder import QueryBuilder
from app.models.historical_incident import HistoricalIncident
from app.signoz.models import TraceRecord

class TelemetryService:
    """
    SigNoz telemetry interface.
    """

    # =====================================================================
    # Internal Parsing Helpers
    # =====================================================================

    def _extract_payload(
        self,
        result: Any,
    ) -> dict[str, Any]:
        """
        Extract JSON payload from MCP CallToolResult.
        """
        if result is None:
            return {}

        logger.debug("Received MCP result of type %s", type(result).__name__)

        if not hasattr(result, "content"):
            return {}

        for content in result.content:

            if isinstance(content, TextContent):

                logger.info(
                    "RAW JSON: %s",
                    content.text,
                )

                try:

                    return json.loads(
                        content.text
                    )

                except json.JSONDecodeError:

                    logger.exception(
                        "Failed to decode MCP JSON."
                    )

                    return {}

        return {}

    def _extract_rows(
        self,
        payload: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Extract rows from SigNoz payload.
        """
        if not payload:
            return []
            
        # Handle different SigNoz response formats
        if "data" in payload:
            data = payload["data"]
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # Handle nested data structures
                if "result" in data and isinstance(data["result"], list):
                    return data["result"]
                elif "rows" in data and isinstance(data["rows"], list):
                    return data["rows"]
        
        # Handle direct list response
        if isinstance(payload, list):
            return payload
            
        logger.warning("Could not extract rows from payload structure: %s", list(payload.keys()))
        return []

    def _trace_to_model(
        self,
        row: dict[str, Any],
    ) -> TraceRecord:
        """
        Convert one SigNoz row into a TraceRecord.
        """
        try:
            return TraceRecord(
                trace_id=row.get("traceID", row.get("trace_id", "")),
                span_id=row.get("spanID", row.get("span_id", "")),
                operation_name=row.get("operationName", row.get("operation_name", "")),
                service_name=row.get("serviceName", row.get("service_name", "")),
                duration=float(row.get("durationNano", row.get("duration", 0))) / 1000000,  # Convert to ms
                start_time=row.get("timestamp", row.get("start_time", "")),
                status_code=row.get("statusCode", row.get("status_code", 0)),
                tags=row.get("tags", {}),
                attributes=row.get("attributes", {}),
                events=row.get("events", []),
                parent_span_id=row.get("parentSpanID", row.get("parent_span_id", "")),
                kind=row.get("kind", ""),
                status_message=row.get("statusMessage", row.get("status_message", ""))
            )
        except Exception as e:
            logger.error("Failed to convert row to TraceRecord: %s", e)
            logger.debug("Problematic row: %s", row)
            # Return minimal valid record
            return TraceRecord(
                trace_id=str(row.get("traceID", row.get("trace_id", "unknown"))),
                span_id=str(row.get("spanID", row.get("span_id", "unknown"))),
                operation_name=str(row.get("operationName", row.get("operation_name", "unknown"))),
                service_name=str(row.get("serviceName", row.get("service_name", "unknown"))),
                duration=0.0,
                start_time="",
                status_code=0,
                tags={},
                attributes={},
                events=[],
                parent_span_id="",
                kind="",
                status_message=""
            )

    def _trace_to_historical(
        self,
        trace: TraceRecord,
    ) -> HistoricalIncident:
        """
        Convert TraceRecord into HistoricalIncident.
        """
        try:
            # Determine incident severity based on trace properties
            severity = "LOW"
            if trace.status_code >= 500:
                severity = "CRITICAL"
            elif trace.status_code >= 400:
                severity = "HIGH"
            elif trace.duration > 10000:  # > 10 seconds
                severity = "MEDIUM"
                
            return HistoricalIncident(
                incident_id=f"hist_{trace.trace_id[:8]}",
                title=f"Historical incident in {trace.service_name}",
                service_name=trace.service_name,
                endpoint=trace.operation_name,
                operation=trace.operation_name,
                environment="production",  # Default
                severity=severity,
                status="RESOLVED",  # Historical incidents are resolved
                root_cause=f"Performance issue in {trace.operation_name}" if trace.duration > 5000 else "Unknown",
                resolution=f"Resolved via {trace.service_name} optimization",
                confidence=min(95, max(10, int((trace.duration / 1000) * 10))),  # Convert duration to confidence score
                similarity_score=0.7,  # Default similarity
                occurrence_count=1,
                resolved_by="system",
                previous_recommendation=f"Monitor {trace.operation_name} performance",
                started_at=datetime.fromisoformat(trace.start_time.replace('Z', '+00:00')) if trace.start_time else None,
                resolved_at=datetime.fromisoformat(trace.start_time.replace('Z', '+00:00')) if trace.start_time else None,
                tags=[trace.service_name, severity.lower()],
                metadata=trace.tags or {}
            )
        except Exception as e:
            logger.error("Failed to convert trace to historical incident: %s", e)
            # Return minimal valid incident
            return HistoricalIncident(
                incident_id=f"hist_{trace.trace_id[:8] if trace.trace_id else 'unknown'}",
                title="Unknown historical incident",
                service_name=trace.service_name or "unknown",
                severity="LOW",
                status="RESOLVED",
                root_cause="Unknown",
                resolution="Unknown",
                confidence=10,
                tags=[],
                metadata={}
            ) 

    def __init__(self) -> None:

        self.gateway = MCPGateway()

        self.query_builder = QueryBuilder()

    # =====================================================================
    # Internal Executor
    # =====================================================================

    async def _execute(
        self,
        tool_name: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute one MCP tool.
        """
        payload = payload or {}

        logger.info(
            "TelemetryService -> %s",
            tool_name,
        )

        result = await self.gateway.execute_tool(
            tool_name,
            payload,
        )

        logger.info("=" * 80)
        logger.info("TOOL NAME: %s", tool_name)
        logger.info("RESULT TYPE: %s", type(result))
        logger.info("FULL RESULT:")
        logger.info("%r", result)
        logger.info("=" * 80)

        return result

    # =====================================================================
    # Traces
    # =====================================================================

    async def search_traces(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_trace_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_search_traces",
            payload,
        )

    async def get_trace_details(
        self,
        trace_id: str,
    ) -> Any:

        return await self._execute(
            "signoz_get_trace_details",
            {
                "trace_id": trace_id,
            },
        )

    async def aggregate_traces(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_trace_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_aggregate_traces",
            payload,
        )

    # =====================================================================
    # Logs
    # =====================================================================

    async def search_logs(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_log_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_search_logs",
            payload,
        )

    async def aggregate_logs(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_log_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_aggregate_logs",
            payload,
        )

    # =====================================================================
    # Metrics
    # =====================================================================

    async def query_metrics(
        self,
        service_name: str,
        metric_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_metric_query(
            service_name=service_name,
            metric_name=metric_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_query_metrics",
            payload,
        )

    async def list_metrics(self) -> Any:

        return await self._execute(
            "signoz_list_metrics",
        )

    async def top_metrics(self) -> Any:

        return await self._execute(
            "signoz_get_top_metrics",
        )

    # =====================================================================
    # Services
    # =====================================================================

    async def list_services(self) -> Any:

        return await self._execute(
            "signoz_list_services",
        )

    async def get_service_top_operations(
        self,
        service_name: str,
    ) -> Any:

        return await self._execute(
            "signoz_get_service_top_operations",
            {
                "service_name": service_name,
            },
        )

    # =====================================================================
    # Dependencies
    # =====================================================================

    async def get_dependencies(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:

        payload = self.query_builder.build_dependency_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_execute_builder_query",
            payload,
        )

    # =====================================================================
    # Historical Traces
    # =====================================================================

    async def get_historical_traces(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:
        """
        Historical traces currently reuse the standard trace search.
        Later this can be extended with explicit time-range filters.
        """

        payload = self.query_builder.build_trace_query(
            service_name=service_name,
            **kwargs,
        )

        return await self._execute(
            "signoz_search_traces",
            payload,
        )

    # =====================================================================
    # Historical Incidents
    # =====================================================================

    async def get_historical_incidents(
        self,
        service_name: str,
        **kwargs,
    ) -> Any:
        """
        Historical incidents currently reuse historical trace search.
        """

        return await self.get_historical_traces(
            service_name=service_name,
            **kwargs,
        )

    # =====================================================================
    # Generic Query Builder
    # =====================================================================

    async def execute_builder_query(
        self,
        payload: dict[str, Any],
    ) -> Any:

        return await self._execute(
            "signoz_execute_builder_query",
            payload,
        )

    # =====================================================================
    # High-Level Conversion Methods
    # =====================================================================

    async def get_traces_as_models(
        self,
        service_name: str,
        **kwargs,
    ) -> list[TraceRecord]:
        """
        Get traces and convert them to TraceRecord models.
        """
        result = await self.search_traces(service_name, **kwargs)
        payload = self._extract_payload(result)
        rows = self._extract_rows(payload)
        
        traces = []
        for row in rows:
            try:
                trace = self._trace_to_model(row)
                traces.append(trace)
            except Exception as e:
                logger.error("Failed to convert row to trace model: %s", e)
                continue
                
        return traces

    async def get_historical_incidents_as_models(
        self,
        service_name: str,
        **kwargs,
    ) -> list[HistoricalIncident]:
        """
        Get historical incidents as HistoricalIncident models.
        """
        traces = await self.get_traces_as_models(service_name, **kwargs)
        
        incidents = []
        for trace in traces:
            try:
                incident = self._trace_to_historical(trace)
                incidents.append(incident)
            except Exception as e:
                logger.error("Failed to convert trace to historical incident: %s", e)
                continue
                
        return incidents

    async def get_logs_as_structured(
        self,
        service_name: str,
        **kwargs,
    ) -> list[dict[str, Any]]:
        """
        Get logs as structured data.
        """
        result = await self.search_logs(service_name, **kwargs)
        payload = self._extract_payload(result)
        return self._extract_rows(payload)

    async def get_metrics_as_structured(
        self,
        service_name: str,
        metric_name: str,
        **kwargs,
    ) -> list[dict[str, Any]]:
        """
        Get metrics as structured data.
        """
        result = await self.query_metrics(service_name, metric_name, **kwargs)
        payload = self._extract_payload(result)
        return self._extract_rows(payload)

    # =====================================================================
    # Health
    # =====================================================================

    async def health_check(self) -> bool:
        """
        Check whether the gateway is connected.
        """
        return await self.gateway.health_check()
