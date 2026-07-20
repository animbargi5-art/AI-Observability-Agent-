from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.agents.correlation_engine import CorrelationEngine


memory = InvestigationMemory()

engine = CorrelationEngine(memory)

result = engine.run()

print("\nCORRELATION RESULT\n")

pprint(result)

print("\nMEMORY\n")

pprint(memory.__dict__)