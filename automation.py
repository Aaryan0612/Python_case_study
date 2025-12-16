import os
import csv
from datetime import datetime

# Import Modules
from vehicle_class import Vehicle
from service_scheduler import MaintenanceScheduler
import maintenance_report

# Setup Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VEHICLE_FILE = os.path.join(SCRIPT_DIR, "vehicles.csv")
HISTORY_FILE = os.path.join(SCRIPT_DIR, "service_history.csv")
REMINDER_LOG = os.path.join(SCRIPT_DIR, "reminders_log.txt")

def save_reminder_log(reg, alerts):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REMINDER_LOG, 'a') as f:
        for alert in alerts:
            f.write(f"[{timestamp}] {reg}: {alert['service']} - {alert['reason']}\n")

def get_service_history(reg_number):
    history_data = {}
    if not os.path.exists(HISTORY_FILE):
        return history_data
    try:
        with open(HISTORY_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Reg_Number'] == reg_number:
                    history_data[row['Service_Type']] = {
                        'date': row['Date'],
                        'mileage': int(row['Mileage'])
                    }
    except: pass 
    return history_data

def log_specific_service(reg_number, service_name):
    print(f"\n--- 📝 Log {service_name} ---")
    cost = input(f"Cost (₹): ")
    provider = input("Provider Name: ")
    mileage = input("Mileage at service: ")
    
    # FIX: Handle Empty Spare Parts input
    parts_input = input("Spare Parts Used (Press Enter for None): ")
    parts = parts_input.strip() if parts_input.strip() else "None"
    
    rating = input("Service Rating (1-5): ")
    date = datetime.now().strftime("%Y-%m-%d")

    file_exists = os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, 'a', newline='') as f:
        fieldnames = ["Reg_Number", "Date", "Service_Type", "Cost", "Mileage", "Provider", "Spare_Parts", "Rating"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists: writer.writeheader()
        
        writer.writerow({
            "Reg_Number": reg_number, "Date": date, "Service_Type": service_name,
            "Cost": cost, "Mileage": mileage, "Provider": provider,
            "Spare_Parts": parts, "Rating": rating
        })
    print("✅ Service Logged.")

def view_full_dashboard():
    """Requirement: Display comprehensive status like the example output."""
    if not os.path.exists(VEHICLE_FILE):
        print("No vehicles found.")
        return

    print("\n" + "="*50)
    print("       VEHICLE SERVICE REMINDER SYSTEM DASHBOARD       ")
    print("="*50)

    # 1. Registered Vehicles
    print("\n--- 🚗 REGISTERED VEHICLES ---")
    with open(VEHICLE_FILE, 'r') as f:
        vehicles = f.readlines()
        for idx, line in enumerate(vehicles):
            parts = line.strip().split(',')
            if len(parts) >= 6:
                print(f"{idx+1}. {parts[0]} {parts[1]} ({parts[5]}) - {parts[3]}")

    # 2. Service History (Last 5 Logs)
    print("\n--- 📜 RECENT SERVICE HISTORY (All Cars) ---")
    if os.path.exists(HISTORY_FILE):
        # Header formatting
        print(f"{'Date':<12} {'Reg Number':<15} {'Service':<20} {'Cost':<10} {'Provider'}")
        print("-" * 70)
        
        with open(HISTORY_FILE, 'r') as f:
            # Read CSV as dictionaries
            reader = list(csv.DictReader(f))
            # Display last 5 entries
            for row in reader[-5:]: 
                print(f"{row['Date']:<12} {row['Reg_Number']:<15} {row['Service_Type']:<20} {row['Cost']:<10} {row['Provider']}")
    else:
        print("No history recorded yet.")

    print("\n" + "="*50)

def main_menu():
    scheduler = MaintenanceScheduler()

    while True:
        print("\n=== 🚘 AUTOMATED VEHICLE SYSTEM (v2.1) ===")
        print("1. Register New Vehicle")
        print("2. Check Reminders & Save Log")
        print("3. Log Maintenance")
        print("4. View Analysis Graphs")
        print("5. View Full Dashboard (Summary)") 
        print("6. Exit")
        
        choice = input("Select: ")

        if choice == '1':
            make = input("Make: "); model = input("Model: ")
            year = input("Year: "); reg = input("Reg: ")
            km = int(input("Mileage: "))
            owner = input("Owner Name: ") 
            v = Vehicle(make, model, year, reg, km, owner)
            v.save_to_file()

        elif choice == '2':
            if not os.path.exists(VEHICLE_FILE):
                print("❌ No vehicles found."); continue
            
            with open(VEHICLE_FILE, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 6: 
                        make, model, year, reg, km, owner = parts[:6]
                        history_dates = get_service_history(reg)
                        due_list = scheduler.get_due_services(int(km), history_dates)
                        
                        if due_list:
                            print(f"\n🔎 {make} {model} ({owner}):")
                            for item in due_list:
                                print(f"   🔴 {item['service']}: {item['reason']}")
                            save_reminder_log(reg, due_list)
                        else:
                            print(f"\n✅ {make} {model}: No urgent services.")

        elif choice == '3':
            reg_input = input("Enter Reg Number: ")
            found_km = None
            if os.path.exists(VEHICLE_FILE):
                with open(VEHICLE_FILE, 'r') as f:
                    for line in f:
                        if reg_input in line:
                            found_km = int(line.strip().split(',')[4])
                            break
            
            if found_km:
                history_dates = get_service_history(reg_input)
                due_list = scheduler.get_due_services(found_km, history_dates)
                if due_list:
                    print(f"\n⚠️ Due Services for {reg_input}:")
                    for item in due_list: print(f"- {item['service']}")
                    if input("Log these? (y/n): ").lower() == 'y':
                        for item in due_list: log_specific_service(reg_input, item['service'])
                
                if input("Log manual service? (y/n): ").lower() == 'y':
                    s_name = input("Service Name: ")
                    log_specific_service(reg_input, s_name)
            else:
                print("Vehicle Not Found.")

        elif choice == '4':
            target = input("Enter Reg Number for Graph: ")
            maintenance_report.generate_report(target)

        elif choice == '5':
            view_full_dashboard()

        elif choice == '6': break

if __name__ == "__main__":
    main_menu()