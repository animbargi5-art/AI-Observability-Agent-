from app.agents.base_agent import BaseAgent
from app.memory.investigation_memory import InvestigationMemory
from app.decision.reasoning_engine import ReasoningEngine


class RootCauseAgent(BaseAgent):

    def __init__(self, memory: InvestigationMemory):

        super().__init__(
            name="Root Cause Agent",
            description="Analyzes all collected evidence to determine the most probable root cause."
        )

        self.memory = memory

        self.reasoning_engine = ReasoningEngine(self.memory)

    def collect_evidence(self):

        return self.memory.evidence

    def group_by_service(self, evidence):

        grouped = {}

        for item in evidence:

            service = (
                item.get("trace", {})
                    .get("service", "Unknown Service")
            )

            grouped.setdefault(service, []).append(item)

        return grouped

    def generate_hypotheses(self, grouped):

        hypotheses = []

        for service, evidence in grouped.items():

            hypotheses.append({
                "service": service,
                "cause": f"Possible issue in {service}",
                "confidence": min(
                    len(evidence) * 20,
                    90
                )
            })

        return hypotheses

    def execute(self):

        evidence = self.collect_evidence()

        graph = self.memory.graph

        nodes = graph.get("nodes", [])

        edges = graph.get("edges", [])

        print(f"Collected Evidence: {len(evidence)}")

        print(f"Graph Nodes: {len(nodes)}")

        print(f"Graph Edges: {len(edges)}")

        # -------------------------------
        # NEW: Run Reasoning Engine
        # -------------------------------

        reasoning = self.reasoning_engine.analyze()

        print("\n========== REASONING ENGINE ==========")
        print(reasoning)
        print("======================================\n")

        # -------------------------------
        # No evidence
        # -------------------------------

        if not evidence:

            hypothesis = {
                "cause": "No evidence available",
                "confidence": 0
            }

            self.memory.add_hypothesis(hypothesis)

            self.memory.set_confidence(0)

            self.memory.add_timeline_event(
                "Root cause analysis completed."
            )

            return {
                "root_cause": None,
                "confidence": 0,
                "reasoning": reasoning
            }

        # -------------------------------
        # Existing logic
        # -------------------------------

        grouped = self.group_by_service(evidence)

        hypotheses = self.generate_hypotheses(grouped)

        best = max(
            hypotheses,
            key=lambda h: h["confidence"]
        )

        # -------------------------------
        # NEW:
        # Improve confidence using reasoning
        # -------------------------------

        highest = reasoning.get("highest_severity", "LOW")

        severity_bonus = {
            "LOW": 0,
            "MEDIUM": 5,
            "HIGH": 10,
            "CRITICAL": 15
        }

        best["confidence"] = min(
            best["confidence"] + severity_bonus.get(highest, 0),
            100
        )

        # -------------------------------
        # Store results
        # -------------------------------

        self.memory.add_hypothesis(best)

        self.memory.set_confidence(best["confidence"])

        self.memory.add_timeline_event(
            "Root cause analysis completed."
        )

        return {
            "root_cause": best["cause"],
            "confidence": best["confidence"],
            "reasoning": reasoning
        }