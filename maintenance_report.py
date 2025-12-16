import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_report():
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

        # 5. Analysis
        total_spent = df['Cost'].sum()
        print(f"\n📊 FINANCIAL REPORT")
        print(f"--------------------")
        print(f"💰 Total Spent: ₹{total_spent}")
        print(f"🔢 Services Logged: {len(df)}")
        
        # 6. Graph Logic (Improved)
        plt.figure(figsize=(10, 6))
        
        # Group by Service Type to sum costs (Fixes duplicate bars issue)
        cost_by_service = df.groupby('Service_Type')['Cost'].sum()
        
        # Plot
        cost_by_service.plot(kind='bar', color='purple', edgecolor='black')
        
        plt.title(f'Maintenance Cost Analysis (Total: ₹{total_spent})')
        plt.xlabel('Service Type')
        plt.ylabel('Cost (₹)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout() # Fits labels nicely
        plt.show()

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("💡 TIP: Your 'service_history.csv' might be corrupted.")
        print("👉 ACTION: Delete 'service_history.csv' manually and try again.")