import asyncio

from app.mcp.session import MCPSession


async def main():

    mcp = MCPSession()

    try:

        print("Connecting to SigNoz MCP...")

        await mcp.connect()

        print("Connected!")

        metrics = await mcp.call_tool(
            "signoz_list_metrics",
            {
                "searchContext": "List all available metrics in my SigNoz instance.",
                "timeRange": "1h",
                "limit": 10,
            },
        )

        print(metrics)

    finally:

        await mcp.disconnect()


if __name__ == "__main__":
    asyncio.run(main())