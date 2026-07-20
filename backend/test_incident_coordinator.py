from pprint import pprint

from app.coordinator.incident_coordinator import IncidentCoordinator

coordinator = IncidentCoordinator()

result = coordinator.start_investigation()

print("\nAGENT RESULTS\n")

pprint(result["results"])

print("\nMEMORY\n")

pprint(result["memory"].__dict__)