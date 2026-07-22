from app.database.investigation_repository import InvestigationRepository

repository = InvestigationRepository()

investigations = repository.get_all_investigations()

print()

print("========== ALL INVESTIGATIONS ==========")

print()

for investigation in investigations:

    print(investigation.id)

    print(investigation.incident_id)

    print(investigation.title)

    print(investigation.severity)

    print(investigation.status)

    print(investigation.confidence)

    print("-----------------------------")