from app.database.investigation_repository import InvestigationRepository

repository = InvestigationRepository()

report = {

    "incident": {

        "id": "INC-001",

        "title": "Payment Service Latency",

        "severity": "HIGH",

        "status": "INVESTIGATING"

    },

    "confidence": 92

}

database_id = repository.save_investigation(report)

print("Saved Investigation ID:", database_id)