from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.agents.report_agent import ReportAgent

memory = InvestigationMemory()

agent = ReportAgent(memory)

result = agent.run()

print("\nREPORT RESULT\n")

pprint(result)

print("\nMEMORY\n")

pprint(memory.__dict__)