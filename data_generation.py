import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data(num_floors, units_per_floor, num_days):
    data = []
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=num_days)
    
    for floor in range(1, num_floors + 1):
        for unit in range(1, units_per_floor + 1):
            num_residents = np.random.randint(1, 5)
            unit_size = np.random.randint(50, 150)  # in square meters
            
            for day in range(num_days):
                current_date = start_date + timedelta(days=day)
                for hour in range(24):
                    timestamp = current_date + timedelta(hours=hour)
                    base_consumption = np.random.normal(10, 2)  # Base consumption in liters
                    resident_factor = num_residents * np.random.uniform(0.8, 1.2)
                    size_factor = (unit_size / 100) * np.random.uniform(0.9, 1.1)
                    time_factor = 1 + 0.5 * np.sin(np.pi * hour / 12)  # Simulating daily patterns
                    
                    water_usage = base_consumption * resident_factor * size_factor * time_factor
                    
                    data.append({
                        'timestamp': timestamp,
                        'floor': floor,
                        'unit': unit,
                        'water_usage': round(water_usage, 2),
                        'num_residents': num_residents,
                        'unit_size': unit_size
                    })
    
    return pd.DataFrame(data)

# Generate data for a building with 10 floors, 5 units per floor, for the last 30 days
df = generate_data(num_floors=10, units_per_floor=5, num_days=30)

# Save the data to a CSV file
df.to_csv('water_consumption_data.csv', index=False)
print("Data generated and saved to 'water_consumption_data.csv'")

# Simulate IoT sensor data streaming
def simulate_iot_sensor(df):
    while True:
        for _, row in df.iterrows():
            # Simulate some real-time variation
            variation = np.random.uniform(0.9, 1.1)
            sensor_data = {
                'timestamp': datetime.now(),
                'floor': row['floor'],
                'unit': row['unit'],
                'water_usage': round(row['water_usage'] * variation, 2)
            }
            yield sensor_data

# Example usage of the IoT sensor simulation
for sensor_reading in simulate_iot_sensor(df):
    print(sensor_reading)
    # In a real scenario, you would send this data to your centralized system
    # time.sleep(1)  # Simulate delay between readings