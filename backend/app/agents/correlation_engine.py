from app.memory.investigation_memory import InvestigationMemory


class CorrelationEngine:
    """
    Correlates evidence collected by all investigation agents.
    """

    def __init__(self, memory: InvestigationMemory):

        self.memory = memory

    def run(self):

        evidence = self.memory.evidence

        print(f"Collected Evidence: {len(evidence)}")

        correlated = []

        service_correlations = {}

        category_groups = {}

        for finding in evidence:

            trace = finding.get("trace", {})

            service = (
                finding.get("root_service")
                or trace.get("service")
                or "Unknown"
            )

            category = finding.get("category", "General")

            duration = trace.get("duration_ms", 0)

            service_correlations.setdefault(
                service,
                {
                    "service": service,
                    "findings": [],
                    "possible_causes":set()
                }
            )

            service_correlations[service]["findings"].append(finding)

            category_groups.setdefault(category, []).append(finding)

            causes = []

            # Slow request correlation
            if duration > 2000:
                causes.append(
                    "Blocking operation or expensive processing detected."
                )
             
                service_correlations[service]["possible_causes"].add(
                    "Blocking operation or expensive processing detected."
                )

            # GET endpoint correlation
            if trace.get("method") == "GET":
                causes.append(
                    "Review endpoint implementation and downstream dependencies."
                )

                service_correlations[service]["possible_causes"].add(
                    "Review endpoint implementation and downstream dependencies"
                )

            if finding.get("type") == "Application Error":

                service_correlations[service]["possible_causes"].add(
                    "Application exception detected."
                )

            if finding.get("type") == "Traffic Spike":

                service_correlations[service]["possible_causes"].add(
                    "Traffic surge may be affecting performance."
                )

            for service, data in service_correlations.items():

                findings = data["findings"]

                severities = [
                    finding.get("severity", "LOW")
                    for finding in findings
                ]

                priority = {
                    "CRITICAL": 4,
                    "HIGH": 3,
                    "MEDIUM": 2,
                    "LOW": 1,
                    "ERROR": 4,
                }

                highest = max(
                    severities,
                    key=lambda x: priority.get(x, 1)
                )

                correlated.append({

                    "service": service,

                    "severity": highest,

                    "total_findings": len(findings),

                    "finding_types": [
                        finding.get("type")
                        for finding in findings
                    ],

                    "possible_causes": sorted(
                        list(data["possible_causes"])
                    )

                })

        # Store correlations inside shared memory
        self.memory.correlations = correlated

        return {

            "total_correlations": len(correlated),

            "correlations": correlated
        }