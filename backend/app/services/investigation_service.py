from app.database.session import SessionLocal
from app.database.models import Investigation

from app.database.investigation_repository import InvestigationRepository
class InvestigationService:

    def __init__(self):

        self.db = SessionLocal()

        self.repository = InvestigationRepository()

    def save(self, report):

        incident = report.get("incident", {})

        investigation = Investigation(

            incident_id=incident.get("id", "UNKNOWN"),

            title=incident.get("title", "Unknown Incident"),

            severity=incident.get("severity", "UNKNOWN"),

            status=incident.get("status", "UNKNOWN"),

            confidence=report.get("confidence", 0),

            report=report

        )

        self.db.add(investigation)

        self.db.commit()

        self.db.refresh(investigation)

        return investigation

    def close(self):

        self.db.close()

    def save_investigation(self, report):

        return self.repository.save_investigation(report)

    def get_all_investigations(self):

        return self.repository.get_all_investigations()

    def get_investigation_by_id(self, investigation_id):

        return self.repository.get_investigation_by_id(
            investigation_id
        )

    def delete_investigation(self, investigation_id):

        return self.repository.delete_investigation(
            investigation_id
        )