import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("ENV SIGNOZ_API_KEY =", os.getenv("SIGNOZ_API_KEY"))
print("=" * 60)


class MCPConfig:

    SERVER_URL = os.getenv(
        "SIGNOZ_MCP_SERVER",
        "http://localhost:8001/mcp",
    )

    API_KEY = os.getenv("SIGNOZ_API_KEY")

    TIMEOUT = 30