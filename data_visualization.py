import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('water_consumption_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set up the plot style
plt.style.use('seaborn')
sns.set_palette("viridis")

# 1. Daily water consumption for a single unit
unit_data = df[(df['floor'] == 1) & (df['unit'] == 1)]
daily_consumption = unit_data.groupby(unit_data['timestamp'].dt.date)['water_usage'].sum()

plt.figure(figsize=(12, 6))
plt.plot(daily_consumption.index, daily_consumption.values)
plt.title('Daily Water Consumption for Unit 1 on Floor 1')
plt.xlabel('Date')
plt.ylabel('Water Consumption (Liters)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('daily_consumption.png')
plt.close()

# 2. Heatmap of water consumption by floor and unit
pivot_data = df.pivot_table(values='water_usage', index='floor', columns='unit', aggfunc='sum')

plt.figure(figsize=(10, 8))
sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd')
plt.title('Total Water Consumption by Floor and Unit')
plt.xlabel('Unit')
plt.ylabel('Floor')
plt.tight_layout()
plt.savefig('consumption_heatmap.png')
plt.close()

# 3. Box plot of water consumption by number of residents
plt.figure(figsize=(10, 6))
sns.boxplot(x='num_residents', y='water_usage', data=df)
plt.title('Water Consumption Distribution by Number of Residents')
plt.xlabel('Number of Residents')
plt.ylabel('Water Consumption (Liters)')
plt.tight_layout()
plt.savefig('consumption_by_residents.png')
plt.close()

# 4. Scatter plot of water consumption vs unit size
plt.figure(figsize=(10, 6))
sns.scatterplot(x='unit_size', y='water_usage', data=df, alpha=0.5)
plt.title('Water Consumption vs Unit Size')
plt.xlabel('Unit Size (sq meters)')
plt.ylabel('Water Consumption (Liters)')
plt.tight_layout()
plt.savefig('consumption_vs_size.png')
plt.close()

print("Visualizations have been saved as PNG files.")