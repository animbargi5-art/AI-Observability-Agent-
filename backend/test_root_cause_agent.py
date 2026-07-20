from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.agents.root_cause_agent import RootCauseAgent

memory = InvestigationMemory()

agent = RootCauseAgent(memory)

result = agent.run()

print("\nROOT CAUSE RESULT\n")

pprint(result)

print("\nMEMORY\n")

pprint(memory.__dict__)