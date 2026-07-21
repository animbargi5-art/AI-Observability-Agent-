from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.agents.report_agent import ReportAgent

memory = InvestigationMemory()

memory.incident = {
    "status": "ACTIVE",
    "title": "Payment Service Latency",
    "severity": "HIGH"
}

memory.confidence = 92

memory.evidence = [
    {
        "severity": "HIGH",
        "type": "Critical Slow API",
        "message": "GET /demo/slow took 3000 ms",
        "trace": {
            "service": "tattva-ai-backend",
            "endpoint": "/demo/slow"
        }
    }
]

memory.recommendations = [
    {
        "priority": "HIGH",
        "title": "Investigate Slow API",
        "description": "Inspect database queries and external services."
    }
]

memory.timeline = [
    "Trace investigation completed.",
    "Logs investigation completed."
]

memory.graph = {
    "nodes": [
        {
            "service": "tattva-ai-backend",
            "severity": "HIGH"
        }
    ],
    "edges": []
}

memory.hypotheses = [
    {
        "cause": "Slow database query",
        "confidence": 92
    }
]

agent = ReportAgent(memory)

report = agent.run()

print("\n========== FINAL REPORT ==========\n")

pprint(report)

print("\n========== MEMORY ==========\n")

pprint(memory.__dict__)