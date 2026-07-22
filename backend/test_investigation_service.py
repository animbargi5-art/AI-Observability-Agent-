from app.services.investigation_service import InvestigationService

service = InvestigationService()

report = {

    "incident": {

        "id": "INC-999",

        "title": "Testing Service Layer",

        "severity": "HIGH",

        "status": "INVESTIGATING"

    },

    "confidence": 95

}

database_id = service.save_investigation(report)

print()

print("Saved using Service Layer")

print("Database ID:", database_id)