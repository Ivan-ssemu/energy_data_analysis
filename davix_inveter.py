import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
#import prettyprint as pp

# Set the display options for pandas
#pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)        # Show all rows
pd.set_option('display.max_columns', None)     # Show all columns
pd.set_option('display.width', 1000)           # Avoid line breaks
pd.set_option('display.colheader_justify', 'center') 
# Load the data
RMU_data = pd.read_csv(r"C:\Users\HP\Desktop\Python\innovex_power_usage.csv")
inverter_data = pd.read_excel(r"C:\Users\HP\Downloads\energy-storage-container-02030500482236-2025-04-14-2025-05-14.xlsx",
                               sheet_name='Sheet0')
df = pd.DataFrame(RMU_data)
df2 = pd.DataFrame(inverter_data)


# Convert the 'time' column to datetime format
df['time_stamp'] = pd.to_datetime(df['time_stamp'], format='%Y-%m-%d %H:%M:%S')
df2['Timestamp'] =pd.to_datetime(df2['Timestamp'], format='%Y-%m-%d %H:%M:%S')

# Set the 'time_stamp' column as the index
df.set_index('time_stamp', inplace=True)
df['hour'] = df.index.floor('h')
df2.set_index('Timestamp', inplace=True)
df2['hour'] = df2.index.floor('h')

# Group by each hour and calculate the mean
mean_per_hour = df.groupby('hour')[['supply_voltage', 'supply_current', 'battery_voltage']].mean().reset_index()
mean_per_hour2 = df2.groupby('hour')[['AC output voltage(V)', 
                                             'AC intput voltage(V)', 
                                             'AC output active power(W)']].mean().reset_index()
#merged_data = pd.merge(mean_per_hour, mean_per_minute2, on='hour', how='outer', suffixes=('_RMU', '_Inverter'))
#print(merged_data.head())

#fill the missing values

#usage by hour
mean_per_hour['power_usage'] = mean_per_hour['supply_voltage'] * mean_per_hour['supply_current']
mean_per_hour2['current_usage'] = mean_per_hour2['AC output active power(W)'] / mean_per_hour2['AC intput voltage(V)']
mean_per_hour2['current_usage_Output_V'] = mean_per_hour2['AC output active power(W)'] / mean_per_hour2['AC output voltage(V)'] #Current Usage using AC output voltage
mean_per_hour['Davix_Energy_Usage(KWh)'] = (mean_per_hour['power_usage'] / 1000) * 1
mean_per_hour2['Inverter_Energy_Usage(KWh)'] = (mean_per_hour2['AC output active power(W)'] / 1000) * 1
#print("\t\t\t\tRMU Data")
#print(mean_per_hour.head(10))
#print("\t\t\t\tInverter Data")
#print(mean_per_hour2.head(10))
merged_df = pd.merge(mean_per_hour, mean_per_hour2, on='hour', how='outer', suffixes=('_RMU', '_Inverter'))
#print(merged_df)

#save merged to csv
#merged_df.to_csv(r"C:\Users\HP\Desktop\Python\merged_data.csv", index=False)
#print(merged_df.tail())
#print(merged_df.describe()['battery_voltage'])
#print(merged_df['battery_voltage'].describe())

#summation of the energy usage in KWh
total_energy_usage = merged_df['Davix_Energy_Usage(KWh)'].sum()
total_energy_usage_inverter = merged_df['Inverter_Energy_Usage(KWh)'].sum()
total_energy_usage_2 = mean_per_hour['Davix_Energy_Usage(KWh)'].sum()
print(f"Total Davix Energy Usage (KWh): {round(total_energy_usage, 4)},{round(total_energy_usage_2, 4)}")
print(f"Total Inverter Energy Usage (KWh): {round(total_energy_usage_inverter, 4)}")

# Calculating the davix energy usage in kWh if the AC input voltage is greater than 220V
filtered_df = merged_df[merged_df['AC intput voltage(V)'] > 220]
#save filtered to csv
#filtered_df.to_csv(r"C:\Users\HP\Desktop\Python\filtered_data.csv", index=False)
total_energy_usage_filtered = filtered_df['Davix_Energy_Usage(KWh)'].sum()
print(f"Total Davix Energy Usage (KWh) with AC input voltage > 220V: {round(total_energy_usage_filtered, 4)}")
print(filtered_df['Davix_Energy_Usage(KWh)'].describe())
print(filtered_df.count())
#save descriptive statistics to txt file
#filtered_df['Davix_Energy_Usage(KWh)'].describe().to_csv(r"C:\Users\HP\Desktop\Python\filtered_data_statistics.txt", sep='\t')

#calculating cost of davix energy usage 
price_per_kWH = 756.2 #price per kWh in Ush
filtered_df['cost_per_hour'] = filtered_df['Davix_Energy_Usage(KWh)'] * price_per_kWH
print(f"Total Cost of Davix Energy Usage (Ush): {round(filtered_df['cost_per_hour'].sum(), 1)}")
print(filtered_df['cost_per_hour'].describe())
#filtered_df['Davix_Energy_Usage(KWh)']['cost_per_hour'].describe().to_csv(r"C:\Users\HP\Desktop\Python\filtered_data_statistics1.txt", sep='\t')


# --- Function to shade night periods ---
def shade_night(ax, df, night_start_hour=19, night_end_hour=6):
    start_date = df['hour'].min().normalize()
    end_date = df['hour'].max().normalize()

    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    for date in date_range:
        night_start = date + pd.Timedelta(hours=night_start_hour)
        night_end = date + pd.Timedelta(days=1, hours=night_end_hour)
        ax.axvspan(night_start, night_end, color='gray', alpha=0.2)

# --- Plotting the combined data ---
plt.figure(figsize=(16, 8))
ax1 = plt.gca()
ax1.plot(mean_per_hour['hour'], mean_per_hour['supply_voltage'], label='Davix Supply Voltage', color='blue')
ax1.plot(mean_per_hour2['hour'], mean_per_hour2['AC output voltage(V)'], label='Inverter Voltage', color='red')
ax1.plot(mean_per_hour['hour'], mean_per_hour['supply_current'], label='Davix Supply Current', color='orange')
ax1.plot(mean_per_hour2['hour'], mean_per_hour2['current_usage'], label='Inverter Current', color='red')
ax1.plot(mean_per_hour['hour'], mean_per_hour['battery_voltage'], label='Davix Battery Voltage', color='green')
ax1.plot(mean_per_hour2['hour'], mean_per_hour2['AC output active power(W)'], label='Inverter Power', color='red')
ax1.plot(mean_per_hour['hour'], mean_per_hour['power_usage'], label='Davix Power Usage', color='purple')
shade_night(ax1, mean_per_hour)  # <-- Add night shading
ax1.set_title('Innovex Power Usage Over Time Davix Vs Inverter (14th April 2025 - 14th May 2025)')
ax1.set_xlabel('Time')
ax1.set_ylabel('Voltage (V) / Current (A)')
ax1.legend()
ax1.grid()
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
plt.xticks(rotation=90)
plt.tight_layout()
#plt.show()

# --- Plotting supply voltage ---
plt.figure(figsize=(16, 8))
ax2 = plt.gca()
ax2.plot(mean_per_hour['hour'], mean_per_hour['supply_voltage'], label='Davix Supply Voltage', color='blue')
ax2.plot(mean_per_hour2['hour'], mean_per_hour2['AC intput voltage(V)'], label='Inverter Voltage', color='red')
shade_night(ax2, mean_per_hour)
ax2.set_title('Innovex Supply Voltage Over Time Davix Vs Inverter(14th April 2025 - 14th May 2025)')
ax2.set_xlabel('Time')
ax2.set_ylabel('Voltage (V)')
ax2.legend()
ax2.grid()
ax2.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
plt.xticks(rotation=90)
plt.tight_layout()
#plt.show()

# --- Plotting supply current ---
plt.figure(figsize=(16, 8))
ax3 = plt.gca()
ax3.plot(mean_per_hour['hour'], mean_per_hour['supply_current'], label='Davix Supply Current', color='orange')
ax3.plot(mean_per_hour2['hour'], mean_per_hour2['current_usage'], label='Inverter Current', color='red')
shade_night(ax3, mean_per_hour)
ax3.set_title('Innovex Supply Current Over Time Davix Vs Inverter (14th April 2025 - 14th May 2025)')
ax3.set_xlabel('Time')
ax3.set_ylabel('Current (A)')
ax3.legend()
ax3.grid()
ax3.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
plt.xticks(rotation=90)
plt.tight_layout()
#plt.show()

# --- Plotting power usage ---
plt.figure(figsize=(16, 8))
ax4 = plt.gca()
ax4.plot(mean_per_hour['hour'], mean_per_hour['power_usage'], label='Davix Power', color='purple')
ax4.plot(mean_per_hour2['hour'], mean_per_hour2['AC output active power(W)'], label='Inverter Power', color='red')

shade_night(ax4, mean_per_hour)
ax4.set_title('Innovex Power Usage Over Time Davix Vs Inverter (14th April 2025 - 14th May 2025)')
ax4.set_xlabel('Time')
ax4.set_ylabel('Power Usage (W)')
ax4.legend()
ax4.grid()
ax4.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
plt.xticks(rotation=90)
plt.tight_layout()
#plt.show()

# Plotting supply voltage, AC output voltage, and AC input voltage
plt.figure(figsize=(16, 8))
ax5 = plt.gca()
ax5.plot(mean_per_hour['hour'], mean_per_hour['supply_voltage'], label='Davix Supply Voltage', color='blue')
ax5.plot(mean_per_hour2['hour'], mean_per_hour2['AC output voltage(V)'], label='Inverter AC Output Voltage', color='yellow')
ax5.plot(mean_per_hour2['hour'], mean_per_hour2['AC intput voltage(V)'], label='Inverter AC Input Voltage', color='green')
shade_night(ax5, mean_per_hour)
ax5.set_title('Innovex Supply Voltage, AC Output Voltage, and AC Input Voltage Over Time (14th April 2025 - 14th May 2025)')
ax5.set_xlabel('Time')
ax5.set_ylabel('Voltage (V)')
ax5.legend()
ax5.grid()
ax5.xaxis.set_major_locator(mdates.HourLocator(interval=6))
ax5.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
plt.xticks(rotation=90)
plt.tight_layout()
#plt.show()