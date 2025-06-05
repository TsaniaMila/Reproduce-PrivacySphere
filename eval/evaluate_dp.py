import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Load original dan DP-applied data
original = pd.read_csv("data/synthetic_sensor_data.csv")
dp = pd.read_csv("data/sensor_data_dp.csv")

# Plot distribusi temperatur
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.hist(original["temperature"], bins=30, alpha=0.7, label="Original")
plt.hist(dp["temperature_dp"], bins=30, alpha=0.7, label="DP")
plt.title("Temperature Distribution")
plt.legend()

# Plot distribusi sound level
plt.subplot(1, 2, 2)
plt.hist(original["sound_level"], bins=30, alpha=0.7, label="Original")
plt.hist(dp["sound_level_dp"], bins=30, alpha=0.7, label="DP")
plt.title("Sound Level Distribution")
plt.legend()

plt.tight_layout()
plt.show()

# Hitung MSE (utility loss)
mse_temp = mean_squared_error(original["temperature"], dp["temperature_dp"])
mse_sound = mean_squared_error(original["sound_level"], dp["sound_level_dp"])

print(f"\nMean Squared Error (Temperature): {mse_temp:.4f}")
print(f"Mean Squared Error (Sound Level): {mse_sound:.4f}")
