from app.services.investigation_service import InvestigationService

service = InvestigationService()

investigations = service.get_all_investigations()

print()

print("========== ALL INVESTIGATIONS ==========")

print()

for investigation in investigations:

    print(investigation.id)

    print(investigation.title)

    print(investigation.severity)

    print("---------------------")