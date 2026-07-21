from app.memory.investigation_memory import InvestigationMemory


class GraphBuilder:
    """
    Builds an evidence graph from the investigation memory.
    """

    def __init__(self, memory: InvestigationMemory):

        self.memory = memory

    def build(self):

        evidence = self.memory.evidence

        nodes = []
        edges = []

        service_nodes = {}
        endpoint_nodes = {}

        node_id = 1

        for finding in evidence:

            trace = finding.get("trace", {})

            service = trace.get("service", "Unknown Service")

            endpoint = trace.get("endpoint", "Unknown Endpoint")

        # ----------------------------
        # Service Node
        # ----------------------------

            if service not in service_nodes:

                service_node = {
                    "id": f"S{node_id}",
                    "type": "SERVICE",
                    "label": service
                }

                service_nodes[service] = service_node

                nodes.append(service_node)

                node_id += 1

        # ----------------------------
        # Endpoint Node
        # ----------------------------

            endpoint_key = f"{service}:{endpoint}"

            if endpoint_key not in endpoint_nodes:

                endpoint_node = {
                    "id": f"P{node_id}",
                    "type": "ENDPOINT",
                    "label": endpoint
                }

                endpoint_nodes[endpoint_key] = endpoint_node

                nodes.append(endpoint_node)

                edges.append({
                    "source": service_nodes[service]["id"],
                    "target": endpoint_node["id"],
                    "relation": "HAS_ENDPOINT"
                })

                node_id += 1

        # ----------------------------
        # Incident Node
        # ----------------------------

            incident_node = {

                "id": f"E{node_id}",

                "type": "INCIDENT",

                "label": finding.get("type", "Incident"),

                "severity": finding.get("severity", "LOW")
            }

            nodes.append(incident_node)

            edges.append({

                "source": endpoint_nodes[endpoint_key]["id"],

                "target": incident_node["id"],

                "relation": "TRIGGERED"

            })

            node_id += 1

        graph = {

            "nodes": nodes,

            "edges": edges

        }

        self.memory.graph = graph

        return graph