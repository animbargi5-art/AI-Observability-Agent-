from pprint import pprint

from app.agents.metrics_agent import MetricsAgent

agent = MetricsAgent()

result = agent.run()

print("\nMETRICS RESULT\n")

pprint(result)