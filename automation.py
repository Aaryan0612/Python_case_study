import os
import csv
from datetime import datetime

# Import YOUR modules
from vehicle_class import Vehicle
from service_scheduler import MaintenanceScheduler
import maintenance_report

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VEHICLE_FILE = os.path.join(SCRIPT_DIR, "vehicles.csv")
HISTORY_FILE = os.path.join(SCRIPT_DIR, "service_history.csv")

def log_service():
    """Requirement: Log completed services to file."""
    print("\n--- 📝 Log Completed Service ---")
    date = datetime.now().strftime("%Y-%m-%d")
    service = input("Service Name (e.g. Oil Change): ")
    cost = input("Cost (₹): ")
    mileage = input("Current Mileage: ")
    provider = input("Provider Name: ") # Case Study Requirement

    # Save to History CSV
    file_exists = os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Service_Type", "Cost", "Mileage", "Provider"])
        writer.writerow([date, service, cost, mileage, provider])
    
    print("✅ Service Logged Successfully!")

def main_menu():
    scheduler = MaintenanceScheduler()

    while True:
        print("\n=== 🚘 AUTOMATED VEHICLE SYSTEM ===")
        print("1. Register New Vehicle")
        print("2. Check Health & Reminders")
        print("3. Log a Maintenance (Service History)")
        print("4. View Cost Analysis Graph")
        print("5. Exit")
        
        choice = input("Select: ")

        if choice == '1':
            # Uses your Vehicle Class
            make = input("Make: ")
            model = input("Model: ")
            year = input("Year: ")
            reg = input("Reg: ")
            km = int(input("Mileage: "))
            v = Vehicle(make, model, year, reg, km)
            v.save_to_file() # Now saves to correct folder!

        elif choice == '2':
            if not os.path.exists(VEHICLE_FILE):
                print("❌ No vehicles found.")
                continue
            
            # Read from CSV and Check Reminders
            with open(VEHICLE_FILE, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 5:
                        make, model, year, reg, km = parts[:5]
                        print(f"\n🔍 Checking {make} {model}...")
                        
                        # Pass a dummy date for now, or add date to CSV later
                        alerts = scheduler.get_upcoming_services(int(km), "2024-01-01") 
                        
                        if alerts:
                            for a in alerts: print(a)
                        else:
                            print("✅ All systems go.")

        elif choice == '3':
            log_service() # Fulfills the "Service History" requirement

        elif choice == '4':
            maintenance_report.generate_report() # Calls your report module

        elif choice == '5':
            break

if __name__ == "__main__":
    main_menu()