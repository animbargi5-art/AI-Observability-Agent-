from app.services.signoz import SigNozService


class DependencyTool:
    """
    Engineering Tool responsible for retrieving
    service dependency information.
    """

    def __init__(self):
        self.signoz = SigNozService()

    def execute(self):
        return self.signoz.get_dependencies()