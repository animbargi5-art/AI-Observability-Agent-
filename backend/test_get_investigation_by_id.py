from app.database.investigation_repository import InvestigationRepository

repository = InvestigationRepository()

investigation = repository.get_investigation_by_id(5)

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