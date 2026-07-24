from app.mcp.session import MCPSession


class SigNozService:

    def __init__(self):
        self.mcp = MCPSession()

    async def ensure_connected(self):
        if self.mcp.session is None:
            await self.mcp.connect()

    async def connect(self):
        await self.ensure_connected()

    async def disconnect(self):
        await self.mcp.disconnect()

    async def list_metrics(
        self,
        search_context: str = "List all available metrics.",
        time_range: str = "24h",
        limit: int = 100,
    ):
        await self.ensure_connected()

        return await self.mcp.call_tool(
            "signoz_list_metrics",
            {
                "searchContext": search_context,
                "timeRange": time_range,
                "limit": limit,
            },
        )

    async def list_services(self):
        await self.ensure_connected()

        return await self.mcp.call_tool(
            "signoz_list_services",
            {
                "searchContext": "List all services in my SigNoz instance.",
                "timeRange": "24h",
            },
        )

    async def search_logs(
        self,
        query: str = "",
        limit: int = 100,
    ):
        await self.ensure_connected()

        return await self.mcp.call_tool(
            "signoz_search_logs",
            {
                "searchContext": "Search application logs.",
                "query": query,
                "timeRange": "24h",
                "limit": limit,
            },
        )

    async def search_traces(
        self,
        limit: int = 50,
    ):
        await self.ensure_connected()

        return await self.mcp.call_tool(
            "signoz_search_traces",
            {
                "searchContext": "Search traces.",
                "timeRange": "24h",
                "limit": limit,
            },
        )

    async def list_dashboards(self):
        await self.ensure_connected()

        return await self.mcp.call_tool(
            "signoz_list_dashboards",
            {
                "searchContext": "List all dashboards.",
            },
        )

    async def list_alerts(self):
        await self.ensure_connected()

        return await self.mcp.call_tool(
            "signoz_list_alerts",
            {
                "searchContext": "List all alerts.",
            },
        )

    async def list_notification_channels(self):
        await self.ensure_connected()

        return await self.mcp.call_tool(
            "signoz_list_notification_channels",
            {
                "searchContext": "List all notification channels.",
            },
        )

    async def list_views(self):
        await self.ensure_connected()

        return await self.mcp.call_tool(
            "signoz_list_views",
            {
                "searchContext": "List all saved views.",
            },
        )