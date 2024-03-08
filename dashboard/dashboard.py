import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

sns.set(style='dark')

#current_dir = os.getcwd()
#relative_path = '/dashboard/day_data.csv'
#absolute_path = os.path.join(current_dir, relative_path)
#with open(absolute_path, 'r') as file:
    #pass

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
    sum_weekly_user_df = df.groupby("count").weekday.sum().sort_values(ascending=False).reset_index()
    return sum_weekly_user_df

def create_sum_monthly_user_df(df):
    sum_monthly_user_df = df.groupby("count").month.sum().sort_values(ascending=False).reset_index()
    return sum_monthly_user_df


# Load cleaned data
day_df = pd.read_csv('./dashboard/day_data.csv')

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


# # Menyiapkan berbagai dataframe
daily_users_df = create_daily_users_df(main_df)
sum_weekly_user_df = create_sum_weekly_user_df(main_df)
sum_monthly_user_df = create_sum_monthly_user_df(main_df)


# plot number of daily users
st.header('Bike Sharing Data')
st.subheader('Daily Report')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_users_df.order_count.sum()
    st.metric("Total users", value=total_orders)

with col2:
    total_bike = daily_users_df.bike.sum() 
    st.metric("Total Bike has been used", value=total_bike)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_users_df["date"],
    daily_users_df["bike"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


# untuk menampilkan pengguna musiman
st.subheader("Seasonal User")

fig_season = plt.figure(figsize=(10,5))

sns.barplot(
    y="count",
    x="season",
    data=day_df,
    hue="year",
)

plt.title("Tren Peminjaman Sepeda pada Musim Tertentu", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel("Musim")
plt.tick_params(axis='x', labelsize=12)

st.pyplot(fig_season)

# pengguna musiman + temp
fig_temp = plt.figure(figsize=(10,6))

sns.scatterplot(x='temp', y='count', data=day_df, hue='season')

plt.xlabel("Temperatur (C)")
plt.ylabel("Tren Peminjaman")
plt.title(None)
plt.tight_layout()

st.pyplot(fig_temp)

# menampilkan pengguna mingguan
st.subheader("Weekly User")

fig_weekly = plt.figure(figsize=(10,5))

sns.barplot(
    y="count",
    x="weekday",
    data=day_df,
    hue="month",
)

plt.title("Tren Peminjaman Sepeda pada Hari tertentu", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel("Hari")
plt.xticks(rotation=45)
plt.tick_params(axis='x', labelsize=12)

st.pyplot(fig_weekly)

# menampilkan pengguna bulanan
st.subheader("Monthly User")

fig_monthly = plt.figure(figsize=(10,5))

sns.barplot(
    y="count",
    x="month",
    data=day_df,
    hue="year",
)

plt.title("Tren Peminjaman Sepeda pada Bulan tertentu", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel("Hari")
plt.xticks(rotation=45)
plt.tick_params(axis='x', labelsize=12)

st.pyplot(fig_monthly)

st.caption('Awaludin Ahmad Hafiz')
