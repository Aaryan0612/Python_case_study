import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_report(target_reg_number=None):
    # 1. Setup Path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "service_history.csv")

    # 2. Check if file exists
    if not os.path.exists(file_path):
        print("\n❌ No service history found! Please 'Log a Maintenance' first.")
        return

    try:
        # 3. Load Data
        df = pd.read_csv(file_path)
        
        # 4. Check for 'Cost' column (Safety check)
        if 'Cost' not in df.columns:
            print("❌ Error: 'Cost' column missing in CSV.")
            return

        # 5. Filter by specific vehicle if requested
        if target_reg_number:
            df = df[df['Reg_Number'] == target_reg_number]
            if df.empty:
                print(f"❌ No history found for vehicle: {target_reg_number}")
                return

        # 6. Analysis Calculations
        total_spent = df['Cost'].sum()
        title_suffix = f"for {target_reg_number}" if target_reg_number else "(All Vehicles)"
        
        print(f"\n📊 FINANCIAL REPORT {title_suffix}")
        print(f"--------------------")
        print(f"💰 Total Amount Spent: ₹{total_spent}")
        print(f"🔢 Total Services Logged: {len(df)}")
        
        # 7. Visualization Logic (Subplots: 2 Graphs in 1 Window)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Graph 1: Bar Chart (Cost Breakdown)
        cost_by_service = df.groupby('Service_Type')['Cost'].sum()
        cost_by_service.plot(kind='bar', color='teal', edgecolor='black', ax=ax1)
        ax1.set_title(f'Cost Breakdown {title_suffix}')
        ax1.set_xlabel('Service Type')
        ax1.set_ylabel('Cost (₹)')
        ax1.grid(axis='y', linestyle='--', alpha=0.5)
        
        # Graph 2: Pie Chart (Frequency Analysis)
        freq = df['Service_Type'].value_counts()
        freq.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'], ax=ax2)
        ax2.set_title(f'Service Frequency {title_suffix}')
        ax2.set_ylabel("") # Hide the annoying 'Service_Type' label on the side

        plt.tight_layout() # Adjust layout so labels don't overlap
        print("✅ Opening Analysis Graphs...")
        plt.show()

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("💡 TIP: Your 'service_history.csv' might be corrupted.")
        print("👉 ACTION: Delete 'service_history.csv' manually and try again.")