import requests

from app.core.settings import settings
class SigNozService:

    def _headers(self):

    headers = {}

    if settings.SIGNOZ_API_KEY:
        headers["SIGNOZ-API-KEY"] = settings.SIGNOZ_API_KEY

    return headers

    def __init__(self):

        self.base_url = settings.SIGNOZ_URL

    def get_traces(self):
        pass

    def get_logs(self):
        pass

    def get_metrics(self):
        pass

    def get_dependencies(self):
        pass