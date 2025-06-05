import pandas as pd
import hashlib
from cryptography.fernet import Fernet
from diffprivlib.mechanisms import Laplace
from sklearn.metrics import mean_squared_error
import os
import logging

# Setup logging
logging.basicConfig(
    filename="access_logs.log",
    filemode="a",  # append mode
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ======== CONFIG ========

ROLE = "researcher"  # Change this for different roles
INPUT_FILE = "data/synthetic_sensor_data.csv"
KEY_FILE = "key.key"
OUTPUT_FILE = f"data/final_output_{ROLE}.csv"

# ======== ACCESS POLICY ========

ACCESS_POLICIES = {
    "admin": ["timestamp", "room", "temperature", "motion", "sound_level"],
    "caregiver": ["timestamp", "room_anon", "temperature", "motion", "sound_level_dp"],
    "researcher": ["timestamp", "room_anon", "temperature_dp", "sound_level_dp"],
    "visitor": ["timestamp", "room_anon"]
}

# ======== TOOLS ========

def pseudonymize(value):
    return hashlib.sha256(value.encode()).hexdigest()[:8]

def apply_dp(series, epsilon, sensitivity):
    mech = Laplace(epsilon=epsilon, sensitivity=sensitivity)
    return series.apply(lambda x: mech.randomise(x))

def load_or_generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    return open(KEY_FILE, "rb").read()

def encrypt_column(series, fernet):
    return series.apply(lambda x: fernet.encrypt(str(x).encode()).decode())

# ======== MAIN FLOW ========

def run_pipeline():
    logging.info(f"Middleware started for role: {ROLE}")
    df = pd.read_csv(INPUT_FILE)
    logging.info(f"Loaded input data from {INPUT_FILE}")
    fernet = Fernet(load_or_generate_key())

    # Step 1: Anonymization
    df["room_anon"] = df["room"].apply(pseudonymize)
    logging.info("Anonymization applied (room → room_anon)")

    # Step 2: Differential Privacy
    df["temperature_dp"] = apply_dp(df["temperature"], epsilon=1.0, sensitivity=1.0)
    df["sound_level_dp"] = apply_dp(df["sound_level"], epsilon=1.0, sensitivity=5.0)
    logging.info("Differential Privacy applied to temperature and sound_level")

    # Step 3: Encryption (example on sound_level_dp)
    df["sound_level_enc"] = encrypt_column(df["sound_level_dp"], fernet)
    logging.info("Encryption applied to sound_level_dp")

    # Step 4: Access control
    allowed_cols = ACCESS_POLICIES.get(ROLE, [])
    available_cols = [col for col in allowed_cols if col in df.columns]
    df_filtered = df[available_cols]
    logging.info(f"Access control enforced for role: {ROLE} (columns: {available_cols})")

    # Output final data
    df_filtered.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"Final filtered data saved to: {OUTPUT_FILE}")
    print(f"\n✅ Final output for role '{ROLE}' saved to: {OUTPUT_FILE}")
    print(df_filtered.head())

if __name__ == "__main__":
    run_pipeline()
