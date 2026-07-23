import requests

from app.core.settings import settings


class TelemetryService:

    def __init__(self):

        self.base_url = settings.SIGNOZ_URL

    def get_traces(self):

        """
        Placeholder.
        Next we will call the SigNoz API here.
        """

        print("Fetching traces from SigNoz...")

        return []

    def get_metrics(self):

        print("Fetching metrics from SigNoz...")

        return []

    def get_logs(self):

        print("Fetching logs from SigNoz...")

        return []