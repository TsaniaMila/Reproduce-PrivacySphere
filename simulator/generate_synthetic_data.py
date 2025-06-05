import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_synthetic_data(num_rows=1000, start_time=None):
    if start_time is None:
        start_time = datetime.now()

    data = []

    for i in range(num_rows):
        timestamp = start_time + timedelta(seconds=i * 30)

        room = random.choice(['living_room', 'kitchen', 'bedroom', 'bathroom'])

        temperature = round(np.random.normal(loc=22, scale=2), 2)
        motion = random.choice([0, 1])  # 0 = no motion, 1 = motion detected
        sound_level = round(np.random.uniform(30, 70), 2)

        data.append([timestamp, room, temperature, motion, sound_level])

    df = pd.DataFrame(data, columns=['timestamp', 'room', 'temperature', 'motion', 'sound_level'])
    return df

if __name__ == "__main__":
    df = generate_synthetic_data(1440)  # 12 hours data (30 seconds interval)
    df.to_csv("data/synthetic_sensor_data.csv", index=False)
    print("Synthetic sensor data saved to data/synthetic_sensor_data.csv")
