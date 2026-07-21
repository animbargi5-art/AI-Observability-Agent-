from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.agents.correlation_engine import CorrelationEngine


memory = InvestigationMemory()

# ---------------------------------------------------
# Simulated Trace Finding
# ---------------------------------------------------

memory.add_evidence({
    "severity": "HIGH",
    "type": "Critical Slow API",
    "category": "Performance",
    "root_service": "tattva-ai-backend",
    "trace": {
        "service": "tattva-ai-backend",
        "endpoint": "/demo/slow",
        "method": "GET",
        "duration_ms": 3000,
        "trace_id": "trace-001"
    }
})

# ---------------------------------------------------
# Simulated Log Finding
# ---------------------------------------------------

memory.add_evidence({
    "severity": "ERROR",
    "type": "Application Error",
    "category": "Application",
    "root_service": "tattva-ai-backend",
    "message": "Internal Server Error",
    "trace_id": "trace-001"
})

# ---------------------------------------------------
# Simulated Metrics Finding
# ---------------------------------------------------

memory.add_evidence({
    "severity": "MEDIUM",
    "type": "Traffic Spike",
    "category": "Infrastructure",
    "root_service": "tattva-ai-backend",
    "metric": {
        "name": "HTTP Request Rate",
        "value": 34
    }
})

# ---------------------------------------------------

engine = CorrelationEngine(memory)

result = engine.run()

print("\n========== CORRELATION RESULT ==========\n")
pprint(result)

print("\n========== MEMORY ==========\n")
pprint(memory.__dict__)