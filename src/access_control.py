import pandas as pd

# Definisi role dan hak aksesnya
ACCESS_POLICIES = {
    "admin": ["timestamp", "room", "temperature", "motion", "sound_level_dp", "room_anon"],
    "caregiver": ["timestamp", "room_anon", "temperature", "motion", "sound_level_dp"],
    "researcher": ["timestamp", "room_anon", "temperature_dp", "sound_level_dp"],
    "visitor": ["timestamp", "room_anon"]
}

def simulate_access(role: str, data_path="data/sensor_data_decrypted.csv"):
    df = pd.read_csv(data_path)

    if role not in ACCESS_POLICIES:
        raise ValueError(f"Unknown role: {role}")

    allowed_cols = ACCESS_POLICIES[role]
    print(f"\n🔓 Role '{role}' has access to columns: {allowed_cols}")
    
    filtered_df = df[[col for col in allowed_cols if col in df.columns]]
    return filtered_df

if __name__ == "__main__":
    # Simulation example: change the role to try
    for role in ["admin", "caregiver", "researcher", "visitor"]:
        result = simulate_access(role)
        print(result.head(3))
        print("-" * 40)
