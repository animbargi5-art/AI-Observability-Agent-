from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from app.graph.state import GraphState

from app.graph.nodes import (
    trace_agent,
    logs_agent,
    metrics_agent,
    dependency_agent,
    decision_engine,
    recommendation_agent,
)

workflow = StateGraph(GraphState)

workflow.add_node("trace", trace_agent)

workflow.add_node("logs", logs_agent)

workflow.add_node("metrics", metrics_agent)

workflow.add_node("dependency", dependency_agent)

workflow.add_node("decision", decision_engine)

workflow.add_node("recommendation", recommendation_agent)

workflow.add_edge(START, "trace")

workflow.add_edge(START, "logs")

workflow.add_edge(START, "metrics")

workflow.add_edge("trace", "dependency")

workflow.add_edge("logs", "dependency")

workflow.add_edge("metrics", "dependency")

workflow.add_edge("dependency", "decision")

workflow.add_edge("decision", "recommendation")

workflow.add_edge("recommendation", END)

graph = workflow.compile()