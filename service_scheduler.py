# from datetime import datetime

# class MaintenanceScheduler:
#     def __init__(self):
#         self.service_intervals = {
#             'oil_change': {'km': 5000, 'months': 6},
#             'tire_rotation': {'km': 10000, 'months': 12},
#             'brake_inspection': {'km': 15000, 'months': 12},
#             'Air filter replacement': {'km': 30000, 'months': 24},
#         }

#     def get_upcoming_services(self, current_mileage, last_service_date_str=None):
#         alerts = []
        
#         # 1. Mileage Check
#         for service, rules in self.service_intervals.items():
#             interval = rules['km']
#             next_due_km = ((current_mileage // interval) + 1) * interval
#             remaining_km = next_due_km - current_mileage
            
#             # Priority Logic
#             if remaining_km <= 500:
#                 priority = "🔴 URGENT"
#             elif remaining_km <= 1500:
#                 priority = "⚠️  HIGH PRIORITY"
#             else:
#                 priority = "MEDIUM"

#             if remaining_km <= 2000: # Only show if somewhat close
#                 alerts.append(f"{priority}: {service} due in {remaining_km} km")

#         # 2. Date Check (Bonus Logic)
#         if last_service_date_str:
#             last_date = datetime.strptime(last_service_date_str, "%Y-%m-%d")
#             months_passed = (datetime.now() - last_date).days / 30
            
#             for service, rules in self.service_intervals.items():
#                 if months_passed >= rules['months']:
#                     alerts.append(f"📅 OVERDUE: {service} (Time Limit Reached)")
        
#         return alerts

from datetime import datetime

class MaintenanceScheduler:
    def __init__(self):
        # Format: 'Service': {'km': interval_km, 'months': interval_months}
        self.service_intervals = {
            'Oil Change': {'km': 5000, 'months': 6},
            'Tire Rotation': {'km': 10000, 'months': 12},
            'Brake Check': {'km': 15000, 'months': 12},
            'Major Service': {'km': 30000, 'months': 24}
        }

    def get_due_services(self, current_mileage, last_service_data={}):
        """
        last_service_data format: 
        {'Oil Change': {'date': '2024-01-01', 'mileage': 4500}, ...}
        """
        due_list = []
        
        for service, rules in self.service_intervals.items():
            is_due = False
            reason = ""
            interval = rules['km']
            
            # --- LOGIC BRANCH 1: HISTORY EXISTS ---
            if service in last_service_data:
                last_km = last_service_data[service]['mileage']
                last_date_str = last_service_data[service]['date']
                
                # Mileage Check based on LAST SERVICE
                next_due_km = last_km + interval
                remaining_km = next_due_km - current_mileage
                
                # Time Check
                try:
                    last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                    months_passed = (datetime.now() - last_date).days / 30
                except:
                    months_passed = 0

                if remaining_km <= 1500:
                    is_due = True
                    reason = f"Due in {remaining_km} km (Last done at {last_km} km)"
                elif months_passed >= rules['months']:
                    is_due = True
                    reason = f"Overdue by time ({int(months_passed)} months)"

            # --- LOGIC BRANCH 2: NO HISTORY (Brand New Car) ---
            else:
                # Check if we are sitting EXACTLY on a due milestone (The Innova Fix)
                if current_mileage > 0 and current_mileage % interval == 0:
                    remaining_km = 0
                    is_due = True
                    reason = "Due NOW (Mileage Interval Reached)"
                else:
                    # Predictive: Find the NEXT milestone
                    next_due_km = ((current_mileage // interval) + 1) * interval
                    remaining_km = next_due_km - current_mileage
                    
                    if remaining_km <= 1500:
                        is_due = True
                        reason = f"Due in {remaining_km} km"

            if is_due:
                due_list.append({'service': service, 'reason': reason})
        
        return due_list