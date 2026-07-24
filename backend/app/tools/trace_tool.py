import json

from app.services.shared_signoz import signoz


class TraceTool:

    def __init__(self):
        self.signoz = signoz

    async def execute(self):
        return await signoz.search_traces()