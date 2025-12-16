from datetime import datetime

class MaintenanceScheduler:
    def __init__(self):
        self.service_intervals = {
            'oil_change': {'km': 5000, 'months': 6},
            'tire_rotation': {'km': 10000, 'months': 12},
            'brake_inspection': {'km': 15000, 'months': 12},
            'Air filter replacement': {'km': 30000, 'months': 24},
        }
    # def check_due_services(self, mileage):
    #     due_services = []
    #     for service, interval in self.service_intervals.items():
    #         if mileage % interval == 0:
    #             due_services.append(service)
    #     return due_services
    
    # def upcoming_services(self, current_mileage, threshold=1000):
    #     upcoming_services = []
    #     for service, interval in self.service_intervals.items():
    #         next_due = ((current_mileage // interval) + 1) * interval
    #         remainig = next_due - current_mileage
    #         if remainig <= threshold:
    #             upcoming_services.append(f"{service} due in {remainig} km")
    #     return upcoming_services

    def get_upcoming_services(self, current_mileage, last_service_date_str=None):
        alerts = []
        
        # 1. Mileage Check
        for service, rules in self.service_intervals.items():
            interval = rules['km']
            next_due_km = ((current_mileage // interval) + 1) * interval
            remaining_km = next_due_km - current_mileage
            
            # Priority Logic
            if remaining_km <= 500:
                priority = "🔴 URGENT"
            elif remaining_km <= 1500:
                priority = "⚠️  HIGH PRIORITY"
            else:
                priority = "MEDIUM"

            if remaining_km <= 2000: # Only show if somewhat close
                alerts.append(f"{priority}: {service} due in {remaining_km} km")

        # 2. Date Check (Bonus Logic)
        if last_service_date_str:
            last_date = datetime.strptime(last_service_date_str, "%Y-%m-%d")
            months_passed = (datetime.now() - last_date).days / 30
            
            for service, rules in self.service_intervals.items():
                if months_passed >= rules['months']:
                    alerts.append(f"📅 OVERDUE: {service} (Time Limit Reached)")
        
        return alerts