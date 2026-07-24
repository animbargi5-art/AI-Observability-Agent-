from app.services.shared_signoz import signoz


class DependencyTool:
    """
    Engineering Tool responsible for retrieving
    service dependency information.
    """

    def __init__(self):
        self.signoz = signoz

    async def execute(self):

        return {
            "dependencies": []
        }