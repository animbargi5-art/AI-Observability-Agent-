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

        for index, finding in enumerate(evidence):

            node = {

                "id": f"E{index + 1}",

                "label": finding.get("type", "Evidence"),

                "severity": finding.get("severity", "LOW"),

                "service": finding.get("trace", {}).get("service"),

                "endpoint": finding.get("trace", {}).get("endpoint")

            }

            nodes.append(node)

        for i in range(len(nodes) - 1):

            edges.append({

                "source": nodes[i]["id"],

                "target": nodes[i + 1]["id"],

                "relation": "related_to"

            })

        graph = {

            "nodes": nodes,

            "edges": edges

        }

        self.memory.graph = graph

        return graph