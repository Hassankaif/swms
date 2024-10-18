import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from math import sqrt

# Load the data
df = pd.read_csv('water_consumption_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Prepare data for a single unit
unit_data = df[(df['floor'] == 1) & (df['unit'] == 1)].set_index('timestamp')
unit_data = unit_data['water_usage'].resample('D').sum()

# Split the data into train and test sets
train_size = int(len(unit_data) * 0.8)
train, test = unit_data[:train_size], unit_data[train_size:]

# Fit SARIMA model
model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
results = model.fit()

# Make predictions
forecast = results.get_forecast(steps=len(test))
forecast_mean = forecast.predicted_mean

# Calculate RMSE
rmse = sqrt(mean_squared_error(test, forecast_mean))
print(f'RMSE: {rmse}')

# Forecast future consumption
future_forecast = results.get_forecast(steps=7)  # Forecast for the next 7 days
print("Forecasted water consumption for the next 7 days:")
print(future_forecast.predicted_mean)

# In a real-world scenario, you would repeat this process for each unit
# and store the predictions for use in the blockchain and visualization components