import argparse

import pandas as pd
from pandas import Timestamp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import WeekdayLocator
import numpy as np
from datetime import datetime

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Generate a burndown chart from a CSV file.')
parser.add_argument('filename', type=str, help='Path to the CSV file')
parser.add_argument('--save', action='store_true', help='Save the plot')
parser.add_argument('--target', type=str, help='Target date in YYYY-MM-DD format')

# Parse the command-line arguments
args = parser.parse_args()

# Read the CSV file specified as a command-line argument
df = pd.read_csv(args.filename)

# Show the first few rows to confirm it's loaded
print(f'<=================== Successfully Loaded the file ===================>')
print(df.head())

# Convert 'Updated' to datetime
df['Updated'] = pd.to_datetime(df['Updated'])

# Sort the DataFrame by the 'Updated' column
df.sort_values('Updated', inplace=True)

# Initialize variables
total_issues = len(df)
y_values = [total_issues]
x_values = [df['Updated'].iloc[0]]

# Calculate total issues over time
for i in range(1, len(df)):
    if df['Resolution'].iloc[i] in ['Done', 'Cancelled']:
        total_issues -= 1
    y_values.append(total_issues)
    x_values.append(df['Updated'].iloc[i])

# Create the burndown chart
plt.figure(figsize=(10, 6))

# Create a formatted title string with the current date and time
current_time = datetime.now().strftime("%d/%m, %H:%M")
title_str = f"Project Burn Down (snapshot {current_time})"

# Generate the date string for filename
date_str = datetime.now().strftime("%Y%m%d%H%M")

# Format X-axis text
plt.tick_params(axis='x', colors='darkgrey', labelsize=8)
plt.xticks(rotation=0)

# Format Y-axis text
plt.tick_params(axis='y', colors='darkgrey')

# Format Grid
plt.grid(True, color='lightgrey')

# Remove box around the graph
plt.box(False)

# Plot the line without points
plt.plot(x_values, y_values, marker='', linestyle='-', color='#2596be', linewidth=2,  label='Burndown')

# Format Y-axis to go down to 0
plt.ylim(0, max(y_values) + 1)

# Format X-axis to show labels every week
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(WeekdayLocator(interval=1))

# Extend x-axis to mid-December
# Convert target date string to Timestamp
if args.target:
    end_date = pd.Timestamp(args.target)
else:
    end_date = Timestamp('2023-12-15')  # Default target date

plt.xlim(x_values[0], end_date)

# Plot the line without points
plt.plot(x_values, y_values, marker='', linestyle='-')

# Adding and extending linear trendline
x_numeric = mdates.date2num(x_values)
z = np.polyfit(x_numeric, y_values, 1)
p = np.poly1d(z)

# Extend trendline x-values to end date
x_extended = np.linspace(x_numeric[0], mdates.date2num(end_date), 100)

plt.plot(mdates.num2date(x_extended), p(x_extended), "r--", color='#be4d25', linewidth=0.8, label='Trend')

plt.xlabel('Date')
plt.ylabel('Total Issues')
plt.title(title_str)
plt.grid(True)
plt.gcf().autofmt_xdate()  # auto-format the x-axis labels to fit them better

# Add a legend
plt.legend()

if args.save:
    plt.savefig(f"{date_str}_SellerConf_PL.png")

plt.show()
