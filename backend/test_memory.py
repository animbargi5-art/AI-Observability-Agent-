from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory

memory = InvestigationMemory()

memory.set_incident({
    "id": "INC-001",
    "service": "payment-service",
    "severity": "HIGH",
    "status": "INVESTIGATING"
})

memory.add_evidence({
    "agent": "Trace Agent",
    "type": "Slow API",
    "endpoint": "/payment",
    "duration_ms": 2145
})

memory.add_timeline_event(
    "Trace investigation completed."
)

memory.add_hypothesis({
    "cause": "Database latency",
    "confidence": 82
})

memory.add_recommendation({
    "action": "Increase database connection pool",
    "confidence": 91
})

memory.set_confidence(91)

memory.set_final_report({
    "summary": "Database latency caused payment slowdown."
})

pprint(memory.__dict__)