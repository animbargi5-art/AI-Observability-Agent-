from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.agents.recommendation_agent import RecommendationAgent

memory = InvestigationMemory()

# Incident
memory.incident = {
    "id": "INC-001",
    "title": "Payment Service Latency",
    "severity": "HIGH",
    "status": "INVESTIGATING"
}

# Evidence
memory.evidence = [
    {
        "severity": "HIGH",
        "type": "Critical Slow API",
        "category": "Performance",
        "root_service": "payment-service",
        "trace": {
            "service": "payment-service",
            "endpoint": "/payment",
            "duration_ms": 3200
        }
    },
    {
        "severity": "CRITICAL",
        "type": "Application Error",
        "category": "Application",
        "root_service": "payment-service",
        "trace": {
            "service": "payment-service",
            "endpoint": "/payment"
        }
    },
    {
        "severity": "MEDIUM",
        "type": "Traffic Spike",
        "category": "Infrastructure",
        "root_service": "payment-service"
    }
]

memory.confidence = 92

memory.hypotheses = [
    {
        "service": "payment-service",
        "cause": "High latency detected in payment-service",
        "confidence": 92
    }
]

agent = RecommendationAgent(memory)

result = agent.run()

print("\n========== RECOMMENDATIONS ==========\n")

pprint(result)

print("\n========== MEMORY ==========\n")

pprint(memory.__dict__)