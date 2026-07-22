from app.database.session import SessionLocal
from app.database.models import Investigation


class InvestigationRepository:
    """
    Handles all database operations for investigations.
    """

    def __init__(self):

        self.db = SessionLocal()

    def save_investigation(self, report):

        incident = report.get("incident", {})

        investigation = Investigation(

            incident_id=incident.get(
                "id",
                "UNKNOWN"
            ),

            title=incident.get(
                "title",
                "Unknown Incident"
            ),

            severity=incident.get(
                "severity",
                "LOW"
            ),

            status=incident.get(
                "status",
                "UNKNOWN"
            ),

            confidence=report.get(
                "confidence",
                0
            ),

            report=report

        )

        self.db.add(investigation)

        self.db.commit()

        self.db.refresh(investigation)

        return investigation.id

    def get_all_investigations(self):
        return (
            self.db
            .query(Investigation)
            .all()
        )

    def get_investigation_by_id(self, investigation_id):
        
        return (
            self.db

            .query(Investigation)

            .filter(
                Investigation.id == investigation_id
            )

            .first()
        )

    def delete_investigation(self, investigation_id):

        investigation = (

            self.db

            .query(Investigation)

            .filter(
                Investigation.id == investigation_id
            )

            .first()

        )

        if investigation is None:

            return False

        self.db.delete(investigation)

        self.db.commit()

        return True