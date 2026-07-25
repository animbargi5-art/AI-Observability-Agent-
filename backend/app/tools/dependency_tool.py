from app.services.shared_signoz import signoz


class DependencyTool:
    """
    Retrieves service dependency information from SigNoz.

    Currently returns an empty dependency list until
    SigNoz exposes an MCP dependency endpoint.
    """

    def __init__(self):
        self.signoz = signoz

    async def execute(self):

        # ----------------------------------------------------
        # Future:
        # return await self.signoz.list_dependencies()
        # ----------------------------------------------------

        return {
            "dependencies": []
        }