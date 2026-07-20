from app.services.signoz import SigNozService


class MetricsTool:
    """
    Engineering Tool responsible for retrieving
    metrics from SigNoz.
    """

    def __init__(self):
        self.signoz = SigNozService()

    def execute(self):
        return self.signoz.get_metrics()