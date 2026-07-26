"""
===============================================================================
TattvaAI - Alert Service
===============================================================================

The AlertService provides a high-level interface for managing alerts in
SigNoz through the MCP Gateway.

Responsibilities
----------------
• List active alerts
• List alert rules
• Get alert details
• Get alert history
• Create alert rules
• Update alert rules
• Delete alert rules

The service hides MCP tool names from the rest of the application.

Flow
----
AI Agent
    ↓
AlertService
    ↓
MCPGateway
    ↓
SigNoz MCP Server

===============================================================================
"""

from __future__ import annotations

from typing import Any

from app.core.logger import logger
from app.signoz.mcp_gateway import MCPGateway


class AlertService:
    """
    High-level service for interacting with SigNoz alerts.
    """

    def __init__(self) -> None:

        self.gateway = MCPGateway()

    # =====================================================================
    # Internal Helper
    # =====================================================================

    async def _execute(
        self,
        tool_name: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:

        logger.info(f"Executing alert tool: {tool_name}")

        return await self.gateway.call_tool(
            tool_name=tool_name,
            arguments=payload or {},
        )

    # =====================================================================
    # Alert Instances
    # =====================================================================

    async def list_alerts(
        self,
        **filters,
    ) -> Any:

        return await self._execute(
            "signoz_list_alerts",
            filters,
        )

    # =====================================================================
    # Alert Rules
    # =====================================================================

    async def list_alert_rules(
        self,
        **filters,
    ) -> Any:

        return await self._execute(
            "signoz_list_alert_rules",
            filters,
        )

    async def get_alert(
        self,
        alert_id: str,
    ) -> Any:

        return await self._execute(
            "signoz_get_alert",
            {
                "id": alert_id,
            },
        )

    async def get_alert_history(
        self,
        alert_id: str,
        **filters,
    ) -> Any:

        payload = {
            "id": alert_id,
            **filters,
        }

        return await self._execute(
            "signoz_get_alert_history",
            payload,
        )

    # =====================================================================
    # Create
    # =====================================================================

    async def create_alert(
        self,
        alert_definition: dict[str, Any],
    ) -> Any:

        return await self._execute(
            "signoz_create_alert",
            alert_definition,
        )

    # =====================================================================
    # Update
    # =====================================================================

    async def update_alert(
        self,
        alert_id: str,
        alert_definition: dict[str, Any],
    ) -> Any:

        payload = {
            "id": alert_id,
            **alert_definition,
        }

        return await self._execute(
            "signoz_update_alert",
            payload,
        )

    # =====================================================================
    # Delete
    # =====================================================================

    async def delete_alert(
        self,
        alert_id: str,
    ) -> Any:

        return await self._execute(
            "signoz_delete_alert",
            {
                "id": alert_id,
            },
        )