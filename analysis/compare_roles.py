import pandas as pd
import os

# Role list
roles = ["caregiver", "visitor", "researcher", "admin"]

# Path data folder
data_dir = "data"

# Dictionary to save DataFrame per role
role_data = {}

print("🔍 Reading file per-role...\n")

for role in roles:
    file_path = os.path.join(data_dir, f"final_output_{role}.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        role_data[role] = df
        print(f"✅ {role} → kolom: {list(df.columns)}")
    else:
        print(f"⚠️ File for role '{role}' not found.")

print("\n📊 Comparison of the number of columns and rows:\n")

for role, df in role_data.items():
    print(f"{role:12} → {df.shape[0]} baris, {df.shape[1]} kolom")

print("\n📌 Available columns per role:")

all_columns = set()
for df in role_data.values():
    all_columns.update(df.columns)

all_columns = sorted(all_columns)

# Column availability boolean table
table = []
for col in all_columns:
    row = [col]
    for role in roles:
        if role in role_data:
            row.append("✔️" if col in role_data[role].columns else "❌")
        else:
            row.append("N/A")
    table.append(row)

# Display as a text table
print(f"\n{'Column':<20} {'Caregiver':<10} {'Visitor':<10} {'Researcher':<10} {'Admin'}")
print("-" * 70)
for row in table:
    print(f"{row[0]:<20} {row[1]:<10} {row[2]:<10} {row[3]:<10} {row[3]}")
