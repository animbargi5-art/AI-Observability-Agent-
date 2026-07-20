from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.decision.investigation_engine import InvestigationEngine

memory = InvestigationMemory()

engine = InvestigationEngine(memory)

result = engine.analyze()

print("\nINVESTIGATION ENGINE\n")

pprint(result)