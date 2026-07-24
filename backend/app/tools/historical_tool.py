from app.services.shared_signoz import signoz


class HistoricalTool:

    def __init__(self):
        self.signoz = signoz

    async def execute(self):
        return {
            "history": []
        }