# from datetime import datetime

# class MaintenanceScheduler:
#     def __init__(self):
#         # Format: 'Service': {'km': interval_km, 'months': interval_months}
#         self.service_intervals = {
#             'Oil Change': {'km': 5000, 'months': 6},
#             'Tire Rotation': {'km': 10000, 'months': 12},
#             'Brake Check': {'km': 15000, 'months': 12},
#             'Major Service': {'km': 30000, 'months': 24},
#             'Air Filter': {'km': 20000, 'months': 12}
#         }

#     def get_full_schedule_status(self, current_mileage, last_service_data={}):
#         """
#         Returns a complete list of all services with their status.
#         Handles Exact Matches, Missed Milestones, and Future Predictions.
#         """
#         schedule = []
        
#         for service, rules in self.service_intervals.items():
#             interval_km = rules['km']
#             interval_time = rules['months']
            
#             # Defaults
#             last_done_str = "Never"
#             status = "OK"
            
#             # --- CASE 1: HISTORY EXISTS ---
#             if service in last_service_data:
#                 last_km = last_service_data[service]['mileage']
#                 last_date = last_service_data[service]['date']
#                 last_done_str = f"{last_date} ({last_km} km)"
                
#                 # Next due based on last service
#                 next_due_km = last_km + interval_km
#                 remaining_km = next_due_km - current_mileage
                
#                 # Time Check
#                 try:
#                     last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
#                     months_passed = (datetime.now() - last_date_obj).days / 30
#                     if months_passed >= interval_time:
#                          status = f"OVERDUE (Time: {int(months_passed)} mo)"
#                 except: pass

#             # --- CASE 2: NO HISTORY (Brand New or Unlogged) ---
#             else:
#                 # Sub-case A: Exact Multiple (e.g., 55000 % 5000 == 0) -> DUE NOW
#                 if current_mileage > 0 and current_mileage % interval_km == 0:
#                     next_due_km = current_mileage
#                     remaining_km = 0
#                     status = "DUE NOW (Milestone Reached)"
                
#                 # Sub-case B: Past the first interval (e.g., 55000 > 30000) -> MISSED
#                 # Logic: We find the milestone we passed most recently
#                 elif current_mileage > interval_km:
#                     passed_milestone = (current_mileage // interval_km) * interval_km
#                     next_due_km = passed_milestone 
#                     remaining_km = next_due_km - current_mileage # Negative value
#                     status = f"MISSED ({abs(remaining_km)} km ago)"
                
#                 # Sub-case C: Normal Upcoming (e.g., 4000 vs 5000) -> FUTURE
#                 else:
#                     next_due_km = interval_km
#                     remaining_km = next_due_km - current_mileage

#             # Final Status Logic (if not already flagged by Time/Missed/Due Now)
#             if status == "OK":
#                 if remaining_km <= 0:
#                     status = "OVERDUE"
#                 elif remaining_km <= 1500:
#                     status = "DUE SOON"
            
#             schedule.append({
#                 "Service": service,
#                 "Interval": f"{interval_km} km / {interval_time} mo",
#                 "Last Done": last_done_str,
#                 "Next Due": f"{next_due_km} km ({remaining_km} km left)",
#                 "Status": status
#             })
            
#         return schedule

#     def get_due_services(self, current_mileage, last_service_data={}):
#         """Returns only the urgent items for alerts."""
#         full_schedule = self.get_full_schedule_status(current_mileage, last_service_data)
#         due_list = []
        
#         # Define what counts as "Bad" enough to alert the user
#         alert_triggers = ["OVERDUE", "DUE SOON", "MISSED", "DUE NOW"]
        
#         for item in full_schedule:
#             # We check if any of the trigger words appear in the status string
#             if any(trigger in item['Status'] for trigger in alert_triggers):
#                 due_list.append({'service': item['Service'], 'reason': item['Status']})
                
#         return due_list

from datetime import datetime

class MaintenanceScheduler:
    def __init__(self):
        # Format: 'Service': {'km': interval_km, 'months': interval_months}
        self.service_intervals = {
            'Oil Change': {'km': 5000, 'months': 6},
            'Tire Rotation': {'km': 10000, 'months': 12},
            'Brake Check': {'km': 15000, 'months': 12},
            'Major Service': {'km': 30000, 'months': 24},
            'Air Filter': {'km': 20000, 'months': 12}
        }

    def get_full_schedule_status(self, current_mileage, last_service_data={}):
        """
        Returns a complete list of all services with their status.
        Handles Exact Matches, Missed Milestones, and Future Predictions.
        """
        schedule = []
        
        for service, rules in self.service_intervals.items():
            interval_km = rules['km']
            interval_time = rules['months']
            
            # Defaults
            last_done_str = "Never"
            status = "OK"
            
            # --- CASE 1: HISTORY EXISTS ---
            if service in last_service_data:
                last_km = last_service_data[service]['mileage']
                last_date = last_service_data[service]['date']
                last_done_str = f"{last_date} ({last_km} km)"
                
                # Next due based on last service
                next_due_km = last_km + interval_km
                remaining_km = next_due_km - current_mileage
                
                # Time Check
                try:
                    last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
                    months_passed = (datetime.now() - last_date_obj).days / 30
                    if months_passed >= interval_time:
                         status = f"OVERDUE (Time: {int(months_passed)} mo)"
                except: pass

            # --- CASE 2: NO HISTORY (Brand New or Unlogged) ---
            else:
                # Sub-case A: Exact Multiple (e.g., 55000 % 5000 == 0) -> DUE NOW
                if current_mileage > 0 and current_mileage % interval_km == 0:
                    next_due_km = current_mileage
                    remaining_km = 0
                    status = "DUE NOW (Milestone Reached)"
                
                # Sub-case B: Past the first interval (e.g., 55000 > 30000) -> MISSED
                # Logic: We find the milestone we passed most recently
                elif current_mileage > interval_km:
                    passed_milestone = (current_mileage // interval_km) * interval_km
                    next_due_km = passed_milestone 
                    remaining_km = next_due_km - current_mileage # Negative value
                    status = f"MISSED ({abs(remaining_km)} km ago)"
                
                # Sub-case C: Normal Upcoming (e.g., 4000 vs 5000) -> FUTURE
                else:
                    next_due_km = interval_km
                    remaining_km = next_due_km - current_mileage

            # Final Status Logic (if not already flagged by Time/Missed/Due Now)
            if status == "OK":
                if remaining_km <= 0:
                    status = "OVERDUE"
                elif remaining_km <= 1500:
                    status = "DUE SOON"
            
            schedule.append({
                "Service": service,
                "Interval": f"{interval_km} km / {interval_time} mo",
                "Last Done": last_done_str,
                "Next Due": f"{next_due_km} km ({remaining_km} km left)",
                "Status": status
            })
            
        return schedule

    def get_due_services(self, current_mileage, last_service_data={}):
        """Returns only the urgent items for alerts."""
        full_schedule = self.get_full_schedule_status(current_mileage, last_service_data)
        due_list = []
        
        # FIX: Check if the status string CONTAINS any of these keywords
        # This catches "MISSED (5000 km ago)" because it contains "MISSED"
        alert_triggers = ["OVERDUE", "DUE SOON", "MISSED", "DUE NOW"]
        
        for item in full_schedule:
            if any(trigger in item['Status'] for trigger in alert_triggers):
                due_list.append({'service': item['Service'], 'reason': item['Status']})
                
        return due_list