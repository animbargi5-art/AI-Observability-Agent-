from pprint import pprint

from app.agents.historical_agent import HistoricalAgent

agent = HistoricalAgent()

result = agent.run()

pprint(result)