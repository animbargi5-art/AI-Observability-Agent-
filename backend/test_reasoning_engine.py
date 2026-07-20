from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.decision.reasoning_engine import ReasoningEngine

memory = InvestigationMemory()

memory.graph = {
    "nodes": [
        {
            "id": "E1",
            "service": "payment-service",
            "endpoint": "/payment",
            "severity": "HIGH",
            "label": "Slow API"
        },
        {
            "id": "E2",
            "service": "mysql",
            "endpoint": "SELECT orders",
            "severity": "CRITICAL",
            "label": "Database Timeout"
        },
        {
            "id": "E3",
            "service": "payment-service",
            "endpoint": "/checkout",
            "severity": "MEDIUM",
            "label": "HTTP Error"
        }
    ],
    "edges": [
        {
            "source": "E1",
            "target": "E2"
        },
        {
            "source": "E2",
            "target": "E3"
        }
    ]
}

engine = ReasoningEngine(memory)

result = engine.analyze()

print("\nREASONING ENGINE\n")

pprint(result)