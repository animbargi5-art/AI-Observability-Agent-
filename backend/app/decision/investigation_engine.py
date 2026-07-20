from app.memory.investigation_memory import InvestigationMemory


class InvestigationEngine:
    """
    Performs intelligent reasoning on the collected investigation graph.
    """

    def __init__(self, memory: InvestigationMemory):

        self.memory = memory

    def analyze(self):

        graph = self.memory.graph

        nodes = graph.get("nodes", [])

        edges = graph.get("edges", [])

        print(f"Graph Nodes : {len(nodes)}")
        print(f"Graph Edges : {len(edges)}")

        return {
            "status": "READY",
            "nodes": len(nodes),
            "edges": len(edges)
        }