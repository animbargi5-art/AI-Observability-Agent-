import json

from app.services.shared_signoz import signoz


class MetricsTool:

    def __init__(self):
        self.signoz = signoz

    async def execute(self):

        result = await self.signoz.list_metrics()

        if hasattr(result, "content"):
            return json.loads(result.content[0].text)

        return result