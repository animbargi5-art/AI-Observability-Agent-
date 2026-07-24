from app.services.shared_signoz import signoz


class AlertTool:

    def __init__(self):
        self.signoz = signoz

    async def execute(self):
        return await self.signoz.list_alerts()