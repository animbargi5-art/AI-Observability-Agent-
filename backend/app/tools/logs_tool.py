from app.services.shared_signoz import signoz


class LogsTool:

    def __init__(self):
        self.signoz = signoz

    async def execute(self):
        return await self.signoz.search_logs()