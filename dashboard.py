import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load data
hour_df = pd.read_csv("hour_data.csv")
day_df = pd.read_csv("day_data.csv")

# Function to calculate hourly rentals average
def calculate_hourly_rentals_avg(hour_df):
    # Convert 'hr' and 'cnt' columns to numeric type if they are not already numeric
    hour_df['hr'] = pd.to_numeric(hour_df['hr'], errors='coerce')
    hour_df['cnt'] = pd.to_numeric(hour_df['cnt'], errors='coerce')

    # Group by 'hr' and calculate the mean of 'cnt'
    hourly_rentals_avg = hour_df.groupby('hr')['cnt'].mean()
    
    return hourly_rentals_avg

# Function to calculate daily rentals average
def calculate_daily_rentals_avg(day_df):
    # Group by 'weekday' and calculate the mean of 'cnt'
    daily_rentals_avg = day_df.groupby('weekday')['cnt'].mean()
    
    return daily_rentals_avg

# Function to calculate monthly rentals average
def calculate_monthly_rentals_avg(day_df):
    # Group by 'mnth' and calculate the mean of 'cnt'
    monthly_rentals_avg = day_df.groupby('mnth')['cnt'].mean()
    
    return monthly_rentals_avg

# Function to calculate seasonal rentals
def calculate_seasonal_rentals(day_df):
    # Group by 'season' and calculate the sum of 'cnt'
    seasonal_rentals = day_df.groupby('season')['cnt'].sum()
    
    # Map season index to season names
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    seasonal_rentals.index = seasonal_rentals.index.map(season_mapping)
    
    return seasonal_rentals

# Menambahkan elemen di sidebar

# Sidebar for selecting year
year_option = st.sidebar.selectbox("Select Year", ["All", 2011, 2012])

# Filter data based on selected year
if year_option == "All":
    filtered_hour_df = hour_df.copy()
    filtered_day_df = day_df.copy()
else:
    filtered_hour_df = hour_df[hour_df['yr'] == year_option]
    filtered_day_df = day_df[day_df['yr'] == year_option]

# Calculate average hourly rentals
hourly_rentals_avg = calculate_hourly_rentals_avg(filtered_hour_df)

# Calculate average daily rentals
daily_rentals_avg = calculate_daily_rentals_avg(filtered_day_df)

# Calculate average monthly rentals
monthly_rentals_avg = calculate_monthly_rentals_avg(filtered_day_df)

# Calculate seasonal rentals
seasonal_rentals = calculate_seasonal_rentals(filtered_day_df)

st.header('Bike Rentals Report')

# Plot the average hourly bike rentals
st.subheader("Average Hourly Bike Rentals")
fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(hourly_rentals_avg, marker='o', color='b')
ax.set_title('Average Hourly Bike Rentals')
ax.set_ylabel('Average Count of Bike Rentals')
ax.grid(True)

# Manipulate data
hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
ax.set_xticks(range(24))
ax.set_xticklabels(hours, rotation=45)
st.pyplot(fig)

# Plot the average daily bike rentals
st.subheader("Average Daily Bike Rentals")
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(daily_rentals_avg, marker='o', color='b')
ax.set_title('Average Bike Rentals by Day')
ax.set_ylabel('Average Count of Bike Rentals')
ax.grid(True)
ax.set_xticks(range(7))
ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
st.pyplot(fig)

# Plot the average monthly bike rentals
st.subheader("Average Monthly Bike Rentals")
fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(monthly_rentals_avg, marker='o', color='b')
ax.set_title('Average Bike Rentals by Month')
ax.set_xlabel('Month')
ax.set_ylabel('Average Count of Bike Rentals')
ax.grid(axis='y')
ax.set_xticks(range(12))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot(fig)

# Plot the total bike rentals by season
st.subheader("Total Bike Rentals by Season")
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(seasonal_rentals.index, seasonal_rentals.values)
ax.set_title('Total Bike Rentals by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Total Count of Bike Rentals')
ax.grid(axis='y')
st.pyplot(fig)
