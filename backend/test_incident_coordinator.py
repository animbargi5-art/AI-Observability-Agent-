from pprint import pprint

from app.coordinator.incident_coordinator import IncidentCoordinator

coordinator = IncidentCoordinator()

result = coordinator.start_investigation()

print("\nSTATUS\n")

print(result["status"])

print("\nTIMESTAMP\n")

print(result["timestamp"])

print("\nEXECUTION TIME\n")

print(result["execution_time_seconds"], "seconds")

print("\nFINAL REPORT\n")

pprint(result["report"])

print("\nRAW RESULTS\n")

pprint(result["raw_results"])

print("\nMEMORY\n")

pprint(result["memory"].__dict__)