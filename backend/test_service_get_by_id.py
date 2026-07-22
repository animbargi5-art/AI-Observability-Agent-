from app.services.investigation_service import InvestigationService

service = InvestigationService()

investigation = service.get_investigation_by_id(6)

print()

print("========== INVESTIGATION ==========")

print()

if investigation:

    print("Database ID :", investigation.id)

    print("Incident ID :", investigation.incident_id)

    print("Title       :", investigation.title)

    print("Severity    :", investigation.severity)

    print("Status      :", investigation.status)

    print("Confidence  :", investigation.confidence)

else:

    print("Investigation not found.")