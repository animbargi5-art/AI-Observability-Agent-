"""
===============================================================================
TattvaAI - SigNoz Query Builder
===============================================================================

This module is responsible for constructing telemetry queries for SigNoz.

Responsibilities
----------------
• Build trace queries
• Build log queries
• Build metric queries
• Build alert queries
• Build dependency queries
• Build service queries

This module DOES NOT:

• Execute HTTP requests
• Call MCP
• Parse responses
• Store telemetry

===============================================================================
"""

from typing import Any

from app.signoz.config import SigNozConfig


class QueryBuilder:
    """
    Centralized builder for SigNoz telemetry queries.
    """

    # =========================================================================
    # Constructor
    # =========================================================================

    def __init__(self):

        self.default_time_range = SigNozConfig.DEFAULT_TIME_RANGE

    # =========================================================================
    # Internal Helper
    # =========================================================================

    def _base_query(
        self,
        service_name: str,
        time_range: str | None = None,
    ) -> dict[str, Any]:
        """
        Build the common query structure shared by all telemetry requests.
        """

        return {
            "service_name": service_name,
            "time_range": time_range or self.default_time_range,
        }

    # =========================================================================
    # Trace Query
    # =========================================================================

    def build_trace_query(
        self,
        service_name: str,
        trace_id: str | None = None,
        time_range: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Build a distributed trace query.
        """

        query = self._base_query(service_name, time_range)

        query.update({
            "trace_id": trace_id,
            "limit": limit or SigNozConfig.DEFAULT_TRACE_LIMIT,
        })

        return query

    # =========================================================================
    # Log Query
    # =========================================================================

    def build_log_query(
        self,
        service_name: str,
        level: str | None = None,
        trace_id: str | None = None,
        keyword: str | None = None,
        time_range: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Build a log search query.
        """

        query = self._base_query(service_name, time_range)

        query.update({
            "level": level,
            "trace_id": trace_id,
            "keyword": keyword,
            "limit": limit or SigNozConfig.DEFAULT_LOG_LIMIT,
        })

        return query

    # =========================================================================
    # Metric Query
    # =========================================================================

    def build_metric_query(
        self,
        service_name: str,
        metric_name: str,
        time_range: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Build a metrics query.
        """

        query = self._base_query(service_name, time_range)

        query.update({
            "metric_name": metric_name,
            "limit": limit or SigNozConfig.DEFAULT_METRIC_LIMIT,
        })

        return query

    # =========================================================================
    # Alert Query
    # =========================================================================

    def build_alert_query(
        self,
        service_name: str,
        severity: str | None = None,
        state: str | None = None,
        time_range: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Build an alert query.
        """

        query = self._base_query(service_name, time_range)

        query.update({
            "severity": severity,
            "state": state,
            "limit": limit or SigNozConfig.DEFAULT_ALERT_LIMIT,
        })

        return query

    # =========================================================================
    # Dependency Query
    # =========================================================================

    def build_dependency_query(
        self,
        service_name: str,
        time_range: str | None = None,
    ) -> dict[str, Any]:
        """
        Build a dependency graph query.
        """

        query = self._base_query(service_name, time_range)

        return query

    # =========================================================================
    # Service Query
    # =========================================================================

    def build_service_query(
        self,
    ) -> dict[str, Any]:
        """
        Build a service discovery query.
        """

        return {
            "time_range": self.default_time_range,
        }

    # =========================================================================
    # Historical Query
    # =========================================================================

    def build_historical_query(
        self,
        service_name: str,
        days: int = 30,
    ) -> dict[str, Any]:
        """
        Build a historical telemetry query.
        """

        return {
            "service_name": service_name,
            "days": days,
        }

    # =========================================================================
    # Custom Query
    # =========================================================================

    def build_custom_query(
        self,
        **filters: Any,
    ) -> dict[str, Any]:
        """
        Build a custom query using arbitrary filters.
        """

        return filters