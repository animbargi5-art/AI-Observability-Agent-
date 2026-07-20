from pprint import pprint

from app.memory.investigation_memory import InvestigationMemory
from app.agents.recommendation_agent import RecommendationAgent

memory = InvestigationMemory()

agent = RecommendationAgent(memory)

result = agent.run()

print("\nRECOMMENDATION RESULT\n")

pprint(result)

print("\nMEMORY\n")

pprint(memory.__dict__)