class Investigator:
    """
    Converts investigation findings into a structured
    investigation report.
    """

    def investigate(self, findings):

        report = []

        for finding in findings:

            trace = finding.get("trace", {})

            report.append({

                "severity": finding.get("severity"),

                "type": finding.get("type"),

                "service": trace.get("service"),

                "endpoint": trace.get("endpoint"),

                "status": trace.get("status"),

                "duration_ms": trace.get("duration_ms"),

                "summary": finding.get("message"),

                "possible_causes": self.get_possible_causes(finding),

                "recommendation": self.get_recommendation(finding)

            })

        return report

    def get_possible_causes(self, finding):

        incident_type = finding.get("type", "").lower()

        if "slow" in incident_type:

            return [
                "Slow database query",
                "External API latency",
                "CPU intensive processing",
                "Missing indexes",
                "Thread starvation"
            ]

        elif "server error" in incident_type:

            return [
                "Unhandled exception",
                "Application bug",
                "Database failure",
                "Dependency unavailable"
            ]

        elif "client error" in incident_type:

            return [
                "Invalid request",
                "Authentication failure",
                "Missing parameters"
            ]

        return [
            "Unknown cause"
        ]

    def get_recommendation(self, finding):

        incident_type = finding.get("type", "").lower()

        if "slow" in incident_type:

            return (
                "Inspect SQL queries, traces, external services "
                "and profile the endpoint."
            )

        elif "server error" in incident_type:

            return (
                "Inspect application logs, stack traces "
                "and recent deployments."
            )

        elif "client error" in incident_type:

            return (
                "Validate incoming request payloads "
                "and API contracts."
            )

        return "Further investigation required."