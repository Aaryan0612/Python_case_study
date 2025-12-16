from vehicle_class import Vehicle
from service_scheduler import MaintenanceScheduler

vehicle = Vehicle("Toyota", "fortuner", 2020, "ABC123", 4800)
scheduler = MaintenanceScheduler()
due_services = scheduler.check_due_services(vehicle.mileage)
upcoming_services = scheduler.upcoming_services(vehicle.mileage, threshold=500)

# print(f"Due services for vehicle {vehicle.reg_number} at mileage {vehicle.mileage}: {due_services}")
print("*"*100)
print("Maintenance Report: \n")
if len(due_services)>0:
    print(f" ⚠️ The following services are due for {vehicle.make} {vehicle.model}: \n")
    for service in due_services:
        print(f" - {service}")
else:
    print(f" ✅ No services are due for {vehicle.make} {vehicle.model} at this time.")
print("*"*100)
if upcoming_services:
    print(f"\n🔔 Upcoming services for {vehicle.make} {vehicle.model}:\n")
    for alert in upcoming_services:
        print(f" - {alert}")
print("*"*100)