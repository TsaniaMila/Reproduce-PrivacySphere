import pandas as pd
from cryptography.fernet import Fernet
import base64
import os

def generate_key():
    """Generate dan simpan key"""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load key dari file"""
    return open("key.key", "rb").read()

def encrypt_column(series, fernet):
    """Enkripsi data numerik dalam kolom"""
    return series.apply(lambda x: fernet.encrypt(str(x).encode()).decode())

def decrypt_column(series, fernet):
    """Dekripsi kolom terenkripsi"""
    return series.apply(lambda x: float(fernet.decrypt(x.encode()).decode()))

def main():
    input_path = "data/sensor_data_anon.csv"
    encrypted_path = "data/sensor_data_encrypted.csv"
    decrypted_path = "data/sensor_data_decrypted.csv"

    df = pd.read_csv(input_path)

    # Generate/load key
    key = generate_key() if not os.path.exists("key.key") else load_key()
    fernet = Fernet(key)

    # Encrypt the sound_level_dp column
    df["sound_level_enc"] = encrypt_column(df["sound_level_dp"], fernet)
    df.to_csv(encrypted_path, index=False)
    print(f"Data terenkripsi disimpan di {encrypted_path}")

    # (Simulation) Description
    df["sound_level_dec"] = decrypt_column(df["sound_level_enc"], fernet)
    df.to_csv(decrypted_path, index=False)
    print(f"Data didekripsi dan disimpan di {decrypted_path}")

if __name__ == "__main__":
    main()
