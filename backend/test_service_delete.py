from app.services.investigation_service import InvestigationService

service = InvestigationService()

deleted = service.delete_investigation(6)

print()

print("Deleted :", deleted)