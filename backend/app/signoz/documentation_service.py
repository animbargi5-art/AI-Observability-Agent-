"""
===============================================================================
TattvaAI - Documentation Service
===============================================================================

The DocumentationService provides access to the official SigNoz
documentation through the SigNoz MCP Server.

Responsibilities
----------------
• Search official SigNoz documentation
• Fetch complete documentation pages
• Hide MCP implementation details from AI agents

Flow
----
AI Agent
    ↓
DocumentationService
    ↓
MCPGateway
    ↓
SigNoz MCP Server
    ↓
Official SigNoz Documentation

===============================================================================
"""

from __future__ import annotations

from typing import Any

from app.core.logger import logger
from app.signoz.mcp_gateway import MCPGateway


class DocumentationService:
    """
    Service responsible for retrieving official SigNoz documentation.
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
        """
        Execute one documentation-related MCP tool.
        """

        logger.info(f"Executing documentation tool: {tool_name}")

        return await self.gateway.call_tool(
            tool_name=tool_name,
            arguments=payload or {},
        )

    # =====================================================================
    # Documentation Search
    # =====================================================================

    async def search_docs(
        self,
        query: str,
    ) -> Any:
        """
        Search official SigNoz documentation.
        """

        return await self._execute(
            "signoz_search_docs",
            {
                "query": query,
            },
        )

    # =====================================================================
    # Fetch Documentation
    # =====================================================================

    async def fetch_doc(
        self,
        path: str,
    ) -> Any:
        """
        Fetch a complete documentation page or section.
        """

        return await self._execute(
            "signoz_fetch_doc",
            {
                "path": path,
            },
        )

    # =====================================================================
    # Combined Search + Fetch
    # =====================================================================

    async def search_and_fetch(
        self,
        query: str,
    ) -> Any:
        """
        Search documentation and return the matching result.

        This method currently performs only the search.
        In a later iteration it can automatically fetch the
        highest-ranked document.
        """

        return await self.search_docs(query)