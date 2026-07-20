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

        for finding in evidence:

            trace = finding.get("trace", {})

            duration = trace.get("duration_ms", 0)

            causes = []

            # Slow request correlation
            if duration > 2000:
                causes.append(
                    "Blocking operation or expensive processing detected."
                )

            # GET endpoint correlation
            if trace.get("method") == "GET":
                causes.append(
                    "Review endpoint implementation and downstream dependencies."
                )

            correlated.append({

                "severity": finding.get("severity"),

                "service": trace.get("service"),

                "endpoint": trace.get("endpoint"),

                "duration_ms": duration,

                "possible_causes": causes,

                "trace": trace
            })

        # Store correlations inside shared memory
        self.memory.correlations = correlated

        return {

            "total_correlations": len(correlated),

            "correlations": correlated
        }