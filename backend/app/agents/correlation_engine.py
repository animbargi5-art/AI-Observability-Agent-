from app.memory.investigation_memory import InvestigationMemory


class CorrelationEngine:
    """
    Correlates evidence collected by all investigation agents.
    """

    def __init__(self, memory: InvestigationMemory):
        self.memory = memory

    def run(self):

        evidence = self.memory.evidence

        print(f"\nCollected Evidence: {len(evidence)}")

        correlated = []

        service_correlations = {}

        # ----------------------------------------
        # Group findings by service
        # ----------------------------------------

        for finding in evidence:

            trace = finding.get("trace", {})

            service = (
                finding.get("root_service")
                or trace.get("service")
                or "Unknown"
            )

            duration = trace.get("duration_ms", 0)

            service_correlations.setdefault(
                service,
                {
                    "service": service,
                    "findings": [],
                    "possible_causes": set()
                }
            )

            service_correlations[service]["findings"].append(finding)

            # ----------------------------------------
            # Basic Rule Engine
            # ----------------------------------------

            if duration > 2000:

                service_correlations[service]["possible_causes"].add(
                    "Blocking operation or expensive processing detected."
                )

            if trace.get("method") == "GET":

                service_correlations[service]["possible_causes"].add(
                    "Review endpoint implementation and downstream dependencies."
                )

            if finding.get("type") == "Application Error":

                service_correlations[service]["possible_causes"].add(
                    "Application exception detected."
                )

            if finding.get("type") == "Traffic Spike":

                service_correlations[service]["possible_causes"].add(
                    "Traffic surge may be affecting performance."
                )

        # ----------------------------------------
        # Build Final Correlations
        # ----------------------------------------

        priority = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1,
            "ERROR": 4,
        }

        for service, data in service_correlations.items():

            findings = data["findings"]

            severities = [
                finding.get("severity", "LOW")
                for finding in findings
            ]

            highest = max(
                severities,
                key=lambda x: priority.get(x, 1)
            )

            # ----------------------------------------
            # Advanced Correlation Rules
            # ----------------------------------------

            has_error = any(
                f.get("type") == "Application Error"
                for f in findings
            )

            has_server_error = any(
                f.get("type") == "Server Error"
                for f in findings
            )

            has_slow = any(
                f.get("type") in [
                    "Slow API",
                    "Critical Slow API",
                    "Performance Warning"
                ]
                for f in findings
            )

            has_traffic = any(
                f.get("type") == "Traffic Spike"
                for f in findings
            )

            if has_error and has_slow:

                data["possible_causes"].add(
                    "Unhandled application exception is causing slow API responses."
                )

            if has_server_error and has_slow:

                data["possible_causes"].add(
                    "Server errors are increasing request latency."
                )

            if has_traffic and has_slow:

                data["possible_causes"].add(
                    "High traffic may be causing request queue buildup."
                )

            correlated.append(

                {

                    "service": service,

                    "severity": highest,

                    "total_findings": len(findings),

                    "finding_types": list(
                        {
                            finding.get("type")
                            for finding in findings
                        }
                    ),

                    "possible_causes": sorted(
                        list(data["possible_causes"])
                    ),

                    "evidence": findings

                }

            )

        # ----------------------------------------
        # Save into shared memory
        # ----------------------------------------

        self.memory.correlations = correlated

        # ----------------------------------------
        # Debug Output
        # ----------------------------------------

        print("\n==============================")
        print("Correlated Incidents")
        print("==============================")

        for incident in correlated:

            print()

            print(f"Service : {incident['service']}")

            print(f"Severity : {incident['severity']}")

            print(f"Findings : {incident['total_findings']}")

            print("Types :")

            for t in incident["finding_types"]:
                print(f"   - {t}")

            print("Possible Causes :")

            for cause in incident["possible_causes"]:
                print(f"   - {cause}")

        print("==============================\n")

        return {

            "total_correlations": len(correlated),

            "correlations": correlated

        }