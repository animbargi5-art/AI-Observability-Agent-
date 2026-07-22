from app.database.investigation_repository import InvestigationRepository

repository = InvestigationRepository()

deleted = repository.delete_investigation(5)

print()

print("Deleted :", deleted)