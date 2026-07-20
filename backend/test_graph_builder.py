from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.graph.graph_builder import GraphBuilder


memory = InvestigationMemory()

memory.add_evidence({

    "type": "Slow API",

    "severity": "HIGH",

    "trace": {

        "service": "payment-service",

        "endpoint": "/payment"
    }

})

memory.add_evidence({

    "type": "Database Timeout",

    "severity": "CRITICAL",

    "trace": {

        "service": "mysql",

        "endpoint": "SELECT orders"
    }

})

builder = GraphBuilder(memory)

graph = builder.build()

print("\nGRAPH\n")

pprint(graph)

print("\nMEMORY\n")

pprint(memory.__dict__)