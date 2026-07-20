from collections import Counter

from app.memory.investigation_memory import InvestigationMemory


class ReasoningEngine:
    """
    Performs reasoning over the investigation graph.
    """

    def __init__(self, memory: InvestigationMemory):

        self.memory = memory

    def analyze(self):

        graph = self.memory.graph

        nodes = graph.get("nodes", [])

        edges = graph.get("edges", [])

        severity_order = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "CRITICAL": 4
        }

        service_counter = Counter()

        highest_severity = "NONE"

        suspicious_services = []

        for node in nodes:

            service = node.get("service", "Unknown")

            severity = node.get("severity", "LOW")

            service_counter[service] += 1

            if severity_order.get(severity, 0) > severity_order.get(highest_severity, 0):
                highest_severity = severity

            if severity in ["HIGH", "CRITICAL"]:

                suspicious_services.append({
                    "service": service,
                    "severity": severity,
                    "endpoint": node.get("endpoint"),
                    "incident": node.get("label")
                })

        reasoning = []

        if not nodes:

            reasoning.append(
                "No evidence graph available."
            )

        else:

            reasoning.append(
                f"Analyzed {len(nodes)} evidence nodes."
            )

            reasoning.append(
                f"Detected {len(edges)} relationships."
            )

            reasoning.append(
                f"Highest severity observed: {highest_severity}."
            )

            if suspicious_services:

                reasoning.append(
                    f"{len(suspicious_services)} high-priority findings detected."
                )

        return {

            "graph_nodes": len(nodes),

            "graph_edges": len(edges),

            "services": dict(service_counter),

            "highest_severity": highest_severity,

            "suspicious_services": suspicious_services,

            "reasoning": reasoning,

            "status": "READY"

        }