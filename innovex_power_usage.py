import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Load the data
usage_data = pd.read_csv(r"C:\Users\HP\Desktop\Python\innovex_power_usage.csv")
df = pd.DataFrame(usage_data)

# Convert the 'time' column to datetime format
df['time_stamp'] = pd.to_datetime(df['time_stamp'], format='%Y-%m-%d %H:%M:%S')

# Set the 'time_stamp' column as the index
df.set_index('time_stamp', inplace=True)
df['minute'] = df.index.floor('min')

# Group by each minute and calculate the mean
mean_per_minute = df.groupby('minute')[['supply_voltage', 'supply_current', 'battery_voltage']].mean().reset_index()

#Power usage by minute
mean_per_minute['power_usage'] = mean_per_minute['supply_voltage'] * mean_per_minute['supply_current']
print(mean_per_minute.head())


# --- Function to shade night periods ---
def shade_night(ax, df, night_start_hour=19, night_end_hour=6):
    start_date = df['minute'].min().normalize()
    end_date = df['minute'].max().normalize()

    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    for date in date_range:
        night_start = date + pd.Timedelta(hours=night_start_hour)
        night_end = date + pd.Timedelta(days=1, hours=night_end_hour)
        ax.axvspan(night_start, night_end, color='gray', alpha=0.2)

# --- Plotting the combined data ---
plt.figure(figsize=(16, 8))
ax1 = plt.gca()
ax1.plot(mean_per_minute['minute'], mean_per_minute['supply_voltage'], label='Supply Voltage', color='blue')
ax1.plot(mean_per_minute['minute'], mean_per_minute['supply_current'], label='Supply Current', color='orange')
ax1.plot(mean_per_minute['minute'], mean_per_minute['battery_voltage'], label='Battery Voltage', color='green')
ax1.plot(mean_per_minute['minute'], mean_per_minute['power_usage'], label='Power Usage', color='purple')
shade_night(ax1, mean_per_minute)  # <-- Add night shading
ax1.set_title('Power Usage Over Time (14th April 2025 - 14th May 2025)')
ax1.set_xlabel('Time')
ax1.set_ylabel('Voltage (V) / Current (A)')
ax1.legend()
ax1.grid()
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# --- Plotting supply voltage ---
plt.figure(figsize=(16, 8))
ax2 = plt.gca()
ax2.plot(mean_per_minute['minute'], mean_per_minute['supply_voltage'], label='Supply Voltage', color='blue')
shade_night(ax2, mean_per_minute)
ax2.set_title('Supply Voltage Over Time (14th April 2025 - 14th May 2025)')
ax2.set_xlabel('Time')
ax2.set_ylabel('Voltage (V)')
ax2.legend()
ax2.grid()
ax2.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# --- Plotting supply current ---
plt.figure(figsize=(16, 8))
ax3 = plt.gca()
ax3.plot(mean_per_minute['minute'], mean_per_minute['supply_current'], label='Supply Current', color='orange')
shade_night(ax3, mean_per_minute)
ax3.set_title('Supply Current Over Time (14th April 2025 - 14th May 2025)')
ax3.set_xlabel('Time')
ax3.set_ylabel('Current (A)')
ax3.legend()
ax3.grid()
ax3.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# --- Plotting power usage ---
plt.figure(figsize=(16, 8))
ax4 = plt.gca()
ax4.plot(mean_per_minute['minute'], mean_per_minute['power_usage'], label='Power Usage', color='purple')
shade_night(ax4, mean_per_minute)
ax4.set_title('Power Usage Over Time (14th April 2025 - 14th May 2025)')
ax4.set_xlabel('Time')
ax4.set_ylabel('Power Usage (W)')
ax4.legend()
ax4.grid()
ax4.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()