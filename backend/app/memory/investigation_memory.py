class InvestigationMemory:

    def __init__(self):

        self.incident = {}

        self.evidence = []

        self.correlations = []

        self.graph = {}

        self.timeline = []

        self.hypotheses = []

        self.recommendations = []

        self.confidence = 0

        self.final_report = None

    def set_incident(self, incident: dict):
        """
        Store information about the current incident.
        """
        self.incident = incident

    def add_evidence(self, evidence: dict):
        """
        Add one piece of evidence collected by an agent.
        """
        self.evidence.append(evidence)

    def add_timeline_event(self, event: str):
        """
        Record an investigation step.
        """
        self.timeline.append(event)

    def add_hypothesis(self, hypothesis: dict):
        """
        Store one hypothesis generated during investigation.
        """
        self.hypotheses.append(hypothesis)

    def add_recommendation(self, recommendation: dict):
        """
        Store one recommendation.
        """
        self.recommendations.append(recommendation)

    def set_confidence(self, score: int):
        """
        Store investigation confidence score.
        """
        self.confidence = score

    def set_final_report(self, report: dict):
        """
        Store the generated investigation report.
        """
        self.final_report = report

    def set_graph(self, graph: dict):
        """
        Store the investigation graph.
        """
        self.graph = graph

    def set_correlations(self, correlations: list):
        """
        Store correlated evidence.
        """
        self.correlations = correlations