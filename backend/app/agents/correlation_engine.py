class CorrelationEngine:

    def correlate(self, findings):

        correlated = []

        for finding in findings:

            trace = finding["trace"]

            duration = trace["duration_ms"]

            causes = []

            if duration > 2000:
                causes.append(
                    "Blocking operation or expensive processing detected."
                )

            if trace["method"] == "GET":
                causes.append(
                    "Review endpoint implementation and downstream dependencies."
                )

            correlated.append({
                "severity": finding["severity"],
                "service": trace["service"],
                "endpoint": trace["endpoint"],
                "duration_ms": duration,
                "possible_causes": causes,
                "trace": trace
            })

        return correlated