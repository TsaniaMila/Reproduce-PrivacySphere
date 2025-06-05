import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from diffprivlib.mechanisms import Laplace
import os

# Load original data
original = pd.read_csv("data/synthetic_sensor_data.csv")

def apply_dp(series, epsilon, sensitivity):
    mech = Laplace(epsilon=epsilon, sensitivity=sensitivity)
    return series.apply(lambda x: mech.randomise(x))

epsilons = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
mse_temp_list = []
mse_sound_list = []

for eps in epsilons:
    temp_dp = apply_dp(original["temperature"], epsilon=eps, sensitivity=1.0)
    sound_dp = apply_dp(original["sound_level"], epsilon=eps, sensitivity=5.0)

    mse_temp = mean_squared_error(original["temperature"], temp_dp)
    mse_sound = mean_squared_error(original["sound_level"], sound_dp)

    mse_temp_list.append(mse_temp)
    mse_sound_list.append(mse_sound)

    print(f"Epsilon: {eps}")
    print(f"  Temperature MSE: {mse_temp:.4f}")
    print(f"  Sound Level MSE: {mse_sound:.4f}")
    print("-" * 30)

# Plot hasil
plt.figure(figsize=(8,5))
plt.plot(epsilons, mse_temp_list, marker='o', label="Temperature MSE")
plt.plot(epsilons, mse_sound_list, marker='o', label="Sound Level MSE")
plt.xlabel("Epsilon (ε)")
plt.ylabel("Mean Squared Error (MSE)")
plt.title("Privacy vs Utility Tradeoff")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
