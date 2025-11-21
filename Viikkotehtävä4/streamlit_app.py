import os
import streamlit as st
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

# Ladataan .env-tiedosto
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "weather_db")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
    )


st.title("Säädata Helsingistä")
st.write("Data päivittyy 15 minuutin välein cron-tehtävän avulla.")

# --- SÄÄDATA ---
conn = get_connection()
weather_df = pd.read_sql(
    """
    SELECT city, temperature, description, timestamp
    FROM weather_data
    ORDER BY timestamp DESC
    LIMIT 50
    """,
    conn,
)
conn.close()

st.subheader("Märkää on luvassa")

if weather_df.empty:
    st.write("Ei vielä säätietoja tietokannassa.")
else:
    st.dataframe(weather_df)

    latest = weather_df.iloc[0]
    st.metric(
        label=f"{latest['city']} ({latest['description']})",
        value=f"{latest['temperature']:.1f} °C",
    )

# --- JOULU / JUHANNUS -COUNTDOWN ---
st.subheader("Päivät jouluun ja juhannukseen")

conn = get_connection()
holiday_df = pd.read_sql(
    """
    SELECT holiday, days_left, timestamp
    FROM holiday_countdown
    ORDER BY timestamp DESC
    """,
    conn,
)
conn.close()

if holiday_df.empty:
    st.write("Ei vielä dataa juhlapyhistä. Odota, että cron ajaa fetch_holidays.py -skriptin.")
else:
    # Otetaan vain uusin rivi per juhla
    latest_per_holiday = holiday_df.drop_duplicates(subset="holiday", keep="first")

    st.dataframe(latest_per_holiday)

    # Erotellaan joulu ja juhannus
    christmas = latest_per_holiday[latest_per_holiday["holiday"].str.contains("Joulu")]
    midsummer = latest_per_holiday[latest_per_holiday["holiday"].str.contains("Juhannus")]

    col1, col2 = st.columns(2)

    with col1:
        if not christmas.empty:
            days = int(christmas.iloc[0]["days_left"])
            if days >= 0:
                st.metric("Päiviä jouluun", f"{days} päivää")
            else:
                st.write("Tämän vuoden joulu on jo ollut.")

    with col2:
        if not midsummer.empty:
            days = int(midsummer.iloc[0]["days_left"])
            if days >= 0:
                st.metric("Päiviä juhannukseen", f"{days} päivää")
            else:
                st.write("Tämän vuoden juhannus on jo ollut.")
