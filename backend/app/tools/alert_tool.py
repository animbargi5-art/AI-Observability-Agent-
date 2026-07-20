from app.services.signoz import SigNozService


class AlertTool:
    """
    Engineering Tool responsible for retrieving
    active alerts from SigNoz.
    """

    def __init__(self):
        self.signoz = SigNozService()

    def execute(self):
        return self.signoz.get_alerts()