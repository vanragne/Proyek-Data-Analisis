import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
import plotly.express as px

sns.set(style='dark')

script_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_dir, "day_data.csv")

def create_daily_users_df(df):
    daily_users_df = df.resample(rule='D', on='date').agg({
        "instant": "nunique",
        "count": "sum"
    })
    daily_users_df = daily_users_df.reset_index()
    daily_users_df.rename(columns={
        "instant": "order_count",
        "count": "bike"
    }, inplace=True)
    
    return daily_users_df

def create_sum_weekly_user_df(df):
    sum_weekly_user_df = df.groupby("weekday")["count"].sum().reset_index()
    return sum_weekly_user_df

def create_sum_monthly_user_df(df):
    sum_monthly_user_df = df.groupby("month")["count"].sum().reset_index()
    return sum_monthly_user_df


# Load cleaned data
day_df = pd.read_csv(filename)

datetime_columns = ["date"]
day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

# Filter data
min_date = day_df["date"].min()
max_date = day_df["date"].max()

with st.sidebar:

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["date"] >= str(start_date)) & 
                (day_df["date"] <= str(end_date))]


## Menyiapkan berbagai dataframe
daily_users_df = create_daily_users_df(main_df)
sum_weekly_user_df = create_sum_weekly_user_df(main_df)
sum_monthly_user_df = create_sum_monthly_user_df(main_df)

st.header('Bike Sharing Data')

# Menampilkan Pengguna harian
st.subheader('Daily Bike Usage (Interactive)')
fig_daily = px.line(
    daily_users_df,
    x="date", y="bike",
    title="Daily Bike Usage",
    labels={"bike": "Number of Bikes", "date": "Date"}
)

st.plotly_chart(fig_daily, use_container_width=True)

# Plot pengguna musiman
fig_season = plt.figure(figsize=(10,5)) 
sns.barplot( 
    x="season", y="count", 
    data=day_df, 
    hue="year", 
) 

plt.title("Tren Peminjaman Sepeda pada Musim Tertentu", loc="center", fontsize=15) 
plt.ylabel(None) 
plt.xlabel("Musim") 
plt.tick_params(axis='x', labelsize=12)

# Plot pengguna vs temperatur
fig_temp = plt.figure(figsize=(10,6)) 
sns.scatterplot( 
    x="temp", y="count", 
    data=day_df, 
    hue="season", 
) 

plt.title(None) 
plt.xlabel("Temperature (C)")
plt.ylabel("Tren Peminjaman")  

# Plot pengguna bulanan
fig_monthly = plt.figure(figsize=(10,5)) 
sns.barplot( 
    x="month",
    y="count",  
    data=day_df, 
    hue="year", 
) 

plt.title("Tren Peminjaman Sepeda pada Bulan tertentu", loc="center", fontsize=15) 
plt.ylabel(None) 
plt.xlabel("Bulan") 
plt.xticks(rotation=45) 
plt.tick_params(axis='x', labelsize=12) 

# Plot pengguna mingguan 
fig_weekly = plt.figure(figsize=(10,5)) 
sns.boxplot(
    x="weekday",
    y="count",  
    data=day_df, 
    hue="year" 
) 

plt.title("Tren Peminjaman Sepeda pada Hari tertentu", loc="center", fontsize=15) 
plt.ylabel(None) 
plt.xlabel("Bulan") 
plt.tick_params(axis='x', labelsize=12) 

## Tab layout 
tab1, tab2, tab3, tab4 = st.tabs(["Seasonal", "Temp Relation", "Weekly", "Monthly"])

# tab pengguna musiman
with tab1:
    st.subheader("Seasonal User")
    st.pyplot(fig_season)

# tab pengguna vs temperatur
with tab2:
    st.subheader("User vs Temp")
    st.pyplot(fig_temp)

# tab pengguna mingguan
with tab3:
    st.subheader("Weekly User")
    st.pyplot(fig_weekly)

# tab pengguna bulanan
with tab4:
    st.subheader("Monthly User")
    st.pyplot(fig_monthly)

st.caption('Awaludin Ahmad Hafiz')

