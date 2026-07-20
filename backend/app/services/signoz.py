import time
import requests

from app.core.settings import settings


class SigNozService:

    def __init__(self):
        self.base_url = settings.SIGNOZ_URL

    def _headers(self):
        headers = {
            "Content-Type": "application/json",
            "SIGNOZ-API-KEY": settings.SIGNOZ_SERVICE_ACCOUNT_KEY
        }

        print("\n========== HEADERS ==========")
        print(headers)
        print("=============================\n")

        return headers

    def _time_range(self):
        """
        Return the last one hour in nanoseconds.
        """

        end = int(time.time() * 1_000_000_000)
        start = end - (60 * 60 * 1_000_000_000)

        return start, end

    def get_services(self):

        start, end = self._time_range()

        url = f"{self.base_url}/api/v2/services"

        payload = {
            "start": str(start),
            "end": str(end),
            "tags": []
        }

        print("\n========== REQUEST ==========")
        print("Base URL:", self.base_url)
        print("URL:", url)
        print("Payload:", payload)
        print(
            "Service Account Key Loaded:",
            bool(settings.SIGNOZ_SERVICE_ACCOUNT_KEY)
        )

        if settings.SIGNOZ_SERVICE_ACCOUNT_KEY:
            print(
                "Key Prefix:",
                settings.SIGNOZ_SERVICE_ACCOUNT_KEY[:20] + "..."
            )

        response = requests.post(
            url=url,
            headers=self._headers(),
            json=payload,
            timeout=30
        )

        print("\n========== RESPONSE ==========")
        print("Status Code:", response.status_code)
        print("Response Body:")
        print(response.text)
        print("==============================\n")

        response.raise_for_status()

        return response.json()

    def get_traces(self):

        start, end = self._time_range()

        url = f"{self.base_url}/api/v5/query_range"

        payload = {
            "schemaVersion": "v1",
            "start": start,
            "end": end,
            "requestType": "raw",
            "compositeQuery": {
                "queries": [
                    {
                        "type": "builder_query",
                        "spec": {
                            "name": "A",
                            "signal": "traces",
                            "stepInterval": None,
                            "disabled": False,
                            "filter": {
                                "expression": ""
                            },
                            "limit": 10,
                            "offset": 0,
                            "order": [
                                {
                                    "key": {
                                        "name": "timestamp"
                                    },
                                    "direction": "desc"
                               }
                            ],
                            "having": {
                                "expression": ""
                            },
                            "selectFields": [
                                {
                                    "name": "service.name",
                                    "fieldDataType": "string",
                                    "signal": "traces",
                                    "fieldContext": "resource"
                                },
                                {
                                    "name": "name",
                                    "fieldDataType": "string",
                                    "signal": "traces"
                                },
                                {
                                    "name": "duration_nano",
                                    "fieldDataType": "",
                                    "signal": "traces",
                                    "fieldContext": "span"
                                },
                                {    
                                    "name": "http_method",
                                    "fieldDataType": "",
                                    "signal": "traces",
                                    "fieldContext": "span"
                                },
                                {
                                    "name": "response_status_code",
                                    "fieldDataType": "",
                                    "signal": "traces",
                                    "fieldContext": "span"
                                }
                            ]
                        }
                   }
                ]
            },
            "formatOptions": {
                "formatTableResultForUI": False,
                "fillGaps": False
            },
            "variables": {}
        }

        response = requests.post(
            url=url,
            headers=self._headers(),
            json=payload,
            timeout=30
        )

        print("Status:", response.status_code)
        print(response.text)

        response.raise_for_status()

        return response.json()

    def get_logs(self):

        start, end = self._time_range()

        url = f"{self.base_url}/api/v5/query_range"

        payload = {
            "schemaVersion": "v1",
            "start": start,
            "end": end,
            "requestType": "raw",
            "compositeQuery": {
                "queries": [
                    {
                        "type": "builder_query",
                        "spec": {
                            "name": "A",
                            "signal": "logs",
                            "stepInterval": None,
                            "disabled": False,
                            "filter": {
                                "expression": ""
                            },
                            "limit": 100,
                            "offset": 0,
                            "order": [
                                {
                                    "key": {
                                        "name": "timestamp"
                                    },
                                    "direction": "desc"
                               },
                               {
                                    "key": {
                                        "name": "id"
                                    },
                                    "direction": "desc"
                                }
                            ],
                            "having": {
                                "expression": ""
                            }
                        }
                    }
                ]   
            },
            "formatOptions": {
                "formatTableResultForUI": False,
                "fillGaps": False
            },
            "variables": {}
        }

        response = requests.post(
            url=url,
            headers=self._headers(),
            json=payload,
            timeout=30
        )

        print("Status:", response.status_code)
        print(response.text)

        response.raise_for_status()

        return response.json()

    def get_metrics(self):

        start, end = self._time_range()

        url = f"{self.base_url}/api/v5/query_range"

        payload = {
            "schemaVersion": "v1",
            "start": start,
            "end": end,
            "requestType": "time_series",
            "compositeQuery": {
                "queries": [
                    {
                        "type": "builder_query",
                        "spec": {
                            "name": "A",
                            "signal": "metrics",
                            "source": "",
                            "stepInterval": None,
                            "disabled": False,
                            "filter": {
                                "expression": ""
                            },
                            "having": {
                                "expression": ""
                            },
                            "aggregations": [
                                {
                                    "metricName": "http.server.duration.bucket",
                                    "timeAggregation": "rate",
                                    "spaceAggregation": "p90"
                                }
                            ]
                        }
                    }
                ]
            },
            "formatOptions": {
                "formatTableResultForUI": False,
                "fillGaps": False
            },
            "variables": {}
        }  
        try:
            response = requests.post(
                url=url,
                headers=self._headers(),
                json=payload,
                timeout=30
            )

            print("Status:", response.status_code)
            print(response.text)

            response.raise_for_status()

            return response.json()
        
        except requests.exceptions.RequestException as ex:

            print("Metrics API Error")
            print(ex)

            return {
                "status": "error",
                "message": str(ex),
                "data": None
            }

    def get_dependencies(self):
        """
        Retrieve service dependency information.

        Currently returns an empty list because the local SigNoz
        instance has no service dependency graph yet.
        This method can later be replaced with the actual
        SigNoz API implementation.
        """

        return {
            "status": "success",
            "dependencies": []
        }
    
    def get_alerts(self):
        """
        Retrieve alerts from SigNoz.

        Currently returns an empty list because there are
        no alert rules configured in the local SigNoz instance.
        """

        return {
            "status": "success",
            "alerts": []
        }