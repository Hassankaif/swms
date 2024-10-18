import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
from time_series_forecasting import prepare_data, train_test_split, ets_forecast, arima_forecast, sarima_forecast, rnn_forecast, lstm_forecast

def hybrid_forecast(train, test, top_n=3):
    models = {
        'ETS': ets_forecast,
        'ARIMA': arima_forecast,
        'SARIMA': sarima_forecast,
        'RNN': rnn_forecast,
        'LSTM': lstm_forecast
    }
    
    results = {}
    for name, model_func in models.items():
        forecast, rmse = model_func(train, test)
        results[name] = {'forecast': forecast, 'rmse': rmse}
    
    # Sort models by RMSE and select top N
    top_models = sorted(results.items(), key=lambda x: x[1]['rmse'])[:top_n]
    
    # Average the forecasts of top N models
    hybrid_forecast = np.mean([model['forecast'] for _, model in top_models], axis=0)
    hybrid_rmse = sqrt(mean_squared_error(test, hybrid_forecast))
    
    return hybrid_forecast, hybrid_rmse, [model for model, _ in top_models]

def apply_hybrid_model(data):
    results = {}
    floors = data['floor'].unique()
    units = data['unit'].unique()
    
    for floor in floors:
        for unit in units:
            unit_data = prepare_data(data, floor, unit)
            if len(unit_data) > 0:
                train, test = train_test_split(unit_data)
                forecast, rmse, top_models = hybrid_forecast(train, test)
                results[(floor, unit)] = {
                    'forecast': forecast,
                    'rmse': rmse,
                    'top_models': top_models
                }
    
    return results

# Load the data
df = pd.read_csv('water_consumption_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Apply hybrid model to all units
hybrid_results = apply_hybrid_model(df)

# Print results and save to CSV
results_df = pd.DataFrame(columns=['Floor', 'Unit', 'RMSE', 'Top Models'])
for (floor, unit), result in hybrid_results.items():
    print(f"Floor {floor}, Unit {unit}:")
    print(f"  RMSE: {result['rmse']:.2f}")
    print(f"  Top Models: {', '.join(result['top_models'])}")
    results_df = results_df.append({
        'Floor': floor,
        'Unit': unit,
        'RMSE': result['rmse'],
        'Top Models': ', '.join(result['top_models'])
    }, ignore_index=True)

results_df.to_csv('hybrid_model_results.csv', index=False)
print("\nHybrid model results saved to 'hybrid_model_results.csv'")