import asyncio

from app.mcp.client import MCPClient


async def main():

    client = MCPClient()

    try:
        await client.connect()

        result = await client.call_tool(
            "signoz_fetch_doc",
            {
                "url": "https://signoz.io/docs/userguide/query-builder-v5/"
            },
        )

        print(result)

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())