from app.services.signoz import SigNozService


class LogsTool:
    """
    Engineering Tool responsible for retrieving logs
    from SigNoz.
    """

    def __init__(self):
        self.signoz = SigNozService()

    def execute(self):
        """
        Fetch raw logs from SigNoz.
        """
        return self.signoz.get_logs()