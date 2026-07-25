import json

from app.services.shared_signoz import signoz


class MetricsTool:

    def __init__(self):
        self.signoz = signoz

    async def execute(self):

        result = await self.signoz.list_metrics()

        print("\n========== METRICS TOOL ==========")
        print(type(result))
        print(result)
        print("==================================\n")

        return result