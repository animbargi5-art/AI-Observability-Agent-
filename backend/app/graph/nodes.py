from app.graph.state import GraphState


def trace_agent(state: GraphState):

    print("Trace Agent Executed")

    return {
        "traces": [
            {
                "trace_id": "trace-001",
                "latency": "180ms",
                "status": "OK"
            }
        ]
    }


def logs_agent(state: GraphState):

    print("Logs Agent Executed")

    return {
        "logs": [
            {
                "level": "ERROR",
                "message": "Database timeout"
            }
        ]
    }


def metrics_agent(state: GraphState):

    print("Metrics Agent Executed")

    return {
        "metrics": [
            {
                "cpu": "72%",
                "memory": "61%"
            }
        ]
    }


def dependency_agent(state: GraphState):

    print("Dependency Agent Executed")

    return {
        "dependencies": [
            {
                "service": "postgres",
                "status": "healthy"
            }
        ]
    }


def decision_engine(state: GraphState):

    print("Decision Engine Executed")

    return {
        "hypotheses": [
            "High database latency is causing the incident."
        ]
    }


def recommendation_agent(state: GraphState):

    print("Recommendation Agent Executed")

    return {
        "recommendations": [
            "Scale the database",
            "Check slow SQL queries"
        ]
    }