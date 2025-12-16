# import os
# class Vehicle:
#     def __init__(self, make, model, year, reg_number, mileage):
#         self.make = make
#         self.model = model
#         self.year = year
#         self.reg_number = reg_number
#         self.mileage = mileage
    
#     def display_details(self):
#         print(f"The Vehicle is {self.make}, {self.model}, of {self.year} with {self.reg_number} and Mileage of {self.mileage} ")
    
#     def update_mileage(self, new_mileage):
#         if new_mileage >= self.mileage:
#             self.mileage = new_mileage
#         else:
#             print("Error: New mileage cannot be less than current mileage.")
    
#     def save_to_file(self):
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         file_path = os.path.join(script_dir, "vehicles.csv")
#         with open(file_path, 'a') as file:
#             file.write(f"{self.make},{self.model},{self.year},{self.reg_number},{self.mileage}\n")
#         print(f"✅ Vehicle saved to {file_path}")
# if __name__ == "__main__":
#     while True:
#         make_input = input("Enter vehicle make (or 'exit' to quit): ")
#         if make_input.lower() == 'exit':
#             break
#         model_input = input("Enter vehicle model: ")
#         year_input = input("Enter vehicle year: ")
#         reg_number_input = input("Enter vehicle registration number: ")
#         mileage_input = int(input("Enter vehicle mileage: "))

#         vehicle = Vehicle(make_input, model_input, year_input, reg_number_input, mileage_input)
#         vehicle.display_details()
#         vehicle.save_to_file()
    
#         new_mileage_input = int(input("Enter new mileage to update: "))
#         vehicle.update_mileage(new_mileage_input)
#         vehicle.display_details()

import os

class Vehicle:
    def __init__(self, make, model, year, reg_number, mileage, owner): # Added owner
        self.make = make
        self.model = model
        self.year = year
        self.reg_number = reg_number
        self.mileage = mileage
        self.owner = owner # Store it

    def display_details(self):
        print(f"Vehicle: {self.make} {self.model} ({self.year}) | Reg: {self.reg_number} | Owner: {self.owner} | Mileage: {self.mileage}")

    def update_mileage(self, new_mileage):
        if new_mileage >= self.mileage:
            self.mileage = new_mileage
        else:
            print("Error: New mileage cannot be less than current mileage.")

    def save_to_file(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "vehicles.csv")
        
        # Save Owner as the last field
        with open(file_path, 'a') as file:
            file.write(f"{self.make},{self.model},{self.year},{self.reg_number},{self.mileage},{self.owner}\n")
        print(f"✅ Vehicle saved to {file_path}")

# This block is for testing this file individually
if __name__ == "__main__":
    while True:
        print("\n--- Test Vehicle Registration ---")
        make_input = input("Make (or 'exit'): ")
        if make_input.lower() == 'exit':
            break
        model_input = input("Model: ")
        year_input = input("Year: ")
        reg_number_input = input("Reg Number: ")
        mileage_input = int(input("Mileage: "))
        owner_input = input("Owner Name: ")

        vehicle = Vehicle(make_input, model_input, year_input, reg_number_input, mileage_input, owner_input)
        vehicle.display_details()
        vehicle.save_to_file()