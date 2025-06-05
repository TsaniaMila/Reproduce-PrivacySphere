import pandas as pd
import hashlib
import os

def pseudonymize(value):
    """Hash string jadi ID anonim (tetap konsisten)"""
    return hashlib.sha256(value.encode()).hexdigest()[:8]

def anonymize_rooms(input_file, output_file):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"{input_file} tidak ditemukan")

    df = pd.read_csv(input_file)
    
    # Change room name to anonymous
    df['room_anon'] = df['room'].apply(pseudonymize)

    # Simpan hasil
    df.to_csv(output_file, index=False)
    print(f"Data dengan anonymized room disimpan di {output_file}")

if __name__ == "__main__":
    anonymize_rooms("data/sensor_data_dp.csv", "data/sensor_data_anon.csv")
