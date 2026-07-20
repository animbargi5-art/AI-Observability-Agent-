from app.services.signoz import SigNozService


class TraceTool:
    """
    Engineering Tool responsible for retrieving traces
    from SigNoz.
    """

    def __init__(self):
        self.signoz = SigNozService()

    def execute(self):
        """
        Fetch raw trace data from SigNoz.
        """
        return self.signoz.get_traces()