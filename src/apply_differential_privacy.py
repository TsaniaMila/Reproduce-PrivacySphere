import pandas as pd
import numpy as np
from diffprivlib.mechanisms import Laplace
import os

def apply_dp_to_column(series, epsilon, sensitivity):
    mech = Laplace(epsilon=epsilon, sensitivity=sensitivity)
    return series.apply(lambda x: mech.randomise(x))

def apply_dp(input_path, output_path, epsilon_temp=1.0, epsilon_sound=1.0):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"{input_path} not found.")

    df = pd.read_csv(input_path)

    # Apply DP to column
    df['temperature_dp'] = apply_dp_to_column(df['temperature'], epsilon=epsilon_temp, sensitivity=1.0)
    df['sound_level_dp'] = apply_dp_to_column(df['sound_level'], epsilon=epsilon_sound, sensitivity=5.0)

    df.to_csv(output_path, index=False)
    print(f"DP-applied data saved to {output_path}")

if __name__ == "__main__":
    input_file = "data/synthetic_sensor_data.csv"
    output_file = "data/sensor_data_dp.csv"
    apply_dp(input_file, output_file)
