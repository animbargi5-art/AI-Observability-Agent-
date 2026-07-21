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
            "NONE": 0,
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "CRITICAL": 4
        }

        service_counter = Counter()

        highest_severity = "NONE"

        suspicious_services = []

        service_lookup = {}

        endpoint_lookup = {}

        incident_lookup = {}

        # -------------------------------------
        # Build lookup tables
        # -------------------------------------

        for node in nodes:

            node_type = node.get("type")

            if node_type == "SERVICE":

                service_lookup[node["id"]] = node["label"]

                service_counter[node["label"]] += 1

            elif node_type == "ENDPOINT":

                endpoint_lookup[node["id"]] = node

            elif node_type == "INCIDENT":

                incident_lookup[node["id"]] = node

        # -------------------------------------
        # Analyze graph relationships
        # -------------------------------------

        for edge in edges:

            if edge.get("relation") != "TRIGGERED":
                continue

            endpoint = endpoint_lookup.get(edge["source"])

            incident = incident_lookup.get(edge["target"])

            if endpoint is None or incident is None:
                continue

            service = "Unknown"

            for relation in edges:

                if (
                    relation.get("relation") == "HAS_ENDPOINT"
                    and relation.get("target") == endpoint["id"]
                ):

                    service = service_lookup.get(
                        relation["source"],
                        "Unknown"
                    )

                    break

            severity = incident.get("severity", "LOW")

            if (
                severity_order[severity]
                >
                severity_order[highest_severity]
            ):

                highest_severity = severity

            if severity in ["HIGH", "CRITICAL"]:

                suspicious_services.append({

                    "service": service,

                    "severity": severity,

                    "endpoint": endpoint.get("label"),

                    "incident": incident.get("label")

                })

        # -------------------------------------
        # Build reasoning summary
        # -------------------------------------

        reasoning = []

        if not nodes:

            reasoning.append(
                "No evidence graph available."
            )

        else:

            reasoning.append(
                f"Analyzed {len(nodes)} graph nodes."
            )

            reasoning.append(
                f"Detected {len(edges)} graph relationships."
            )

            reasoning.append(
                f"Detected {len(service_counter)} services."
            )

            reasoning.append(
                f"Highest severity observed: {highest_severity}."
            )

            if suspicious_services:

                reasoning.append(
                    f"{len(suspicious_services)} high-priority incidents detected."
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