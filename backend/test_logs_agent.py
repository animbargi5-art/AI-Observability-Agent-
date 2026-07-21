from pprint import pprint

from app.agents.logs_agent import LogsAgent


agent = LogsAgent()

result = agent.execute()

print("\nRESULT\n")

pprint(result)