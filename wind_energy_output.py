import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value
df = pd.read_csv(r"C:\Users\HP\Desktop\Python\hypothetical_wind_turbine_data.csv")
wind_speed_profile = df["Wind Speed (m/s)"]

print(df.describe())
print(df.info())
#wind turbine parameters
cut_in_speed = 3.5  # m/s
rated_speed = 15.0  # m/s
cut_out_speed = 25.0  # m/s
maximun_power_output = 1500  # kW

# Maintenance hours
maintenance_hours = [20,21,22,23]
lp_problem = LpProblem("Maximize_Energy_output", LpMaximize)

power_output = LpVariable.dicts("PowerOutput",
                                range(24),
                                lowBound=0,
                                upBound=maximun_power_output,
                                cat='Continuous')
lp_problem += lpSum([power_output[hour] for hour in range(24)])

#Loop through each hour to set constraints
for hour in range(24):
    wind_speed = wind_speed_profile[hour]
    lp_problem += power_output[hour] <= (wind_speed >= cut_in_speed) * \
                    (wind_speed <= cut_out_speed) * maximun_power_output
    
    if hour in maintenance_hours:
        lp_problem += power_output[hour] == 0
    lp_problem += power_output[hour] <= maximun_power_output

lp_problem.solve()
optimal_output = [value(power_output[hour]) for hour in range(24)]

total_optimized_output = sum(optimal_output)

#plotting the results

plt.figure(figsize=(10, 6))
plt.plot(optimal_output, drawstyle='steps-post', marker='o',
         linestyle='-', color='green')
plt.fill_between(range(24), optimal_output, step="post", alpha=0.4, color='green')
plt.title('Optimal Power Output over 24 Hours')
plt.xlabel('Hour of the day')
plt.ylabel('Power Output (kW)')
plt.grid(axis='y', linestyle='--')
plt.show()

print(f"status: {LpStatus[lp_problem.status]}")
print(f"Optimal Power Output Schedule: {optimal_output}")
print(f"Total Optimized Power Output: {total_optimized_output} KW")

