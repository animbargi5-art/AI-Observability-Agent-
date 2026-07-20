class Investigator:

    def investigate(self, findings):

        report = []

        for finding in findings:

            trace = finding["trace"]

            report.append({

                "severity": finding["severity"],

                "service": trace["service"],

                "endpoint": trace["endpoint"],

                "summary": (
                    f"{trace['endpoint']} is taking "
                    f"{trace['duration_ms']} ms."
                ),

                "possible_causes": [

                    "Slow database query",

                    "External API latency",

                    "Blocking synchronous code",

                    "CPU-intensive processing"

                ],

                "recommendation": (

                    "Inspect database queries, "

                    "external dependencies, "

                    "and profile the endpoint."

                )

            })

        return report