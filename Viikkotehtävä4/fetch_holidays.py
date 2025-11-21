#!/usr/bin/env python3
import json
import requests
import mysql.connector
from datetime import datetime, date
from dotenv import load_dotenv
import os

# Lataa .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "weather_db")

# Haetaan juhlapyhät API:sta (Suomi 2025)
URL = "https://date.nager.at/api/v3/PublicHolidays/2025/FI"

def days_until(target_date: date):
    today = date.today()
    return (target_date - today).days

def main():
    # Yhdistä tietokantaan
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # Luo taulu (jos puuttuu)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS holiday_countdown (
            id INT AUTO_INCREMENT PRIMARY KEY,
            holiday VARCHAR(50),
            days_left INT,
            timestamp DATETIME
        )
        """
    )

    # Hae API-data
    resp = requests.get(URL, timeout=10)
    data = resp.json()

    # Etsitään Jouluaatto ja Juhannus
    christmas_date = None
    midsummer_date = None

    for item in data:
        if item["localName"] == "Jouluaatto":
            christmas_date = date.fromisoformat(item["date"])
        if item["localName"] == "Juhannuspäivä":
            midsummer_date = date.fromisoformat(item["date"])

    # Laske päivät
    timestamp = datetime.now()

    if christmas_date:
        cursor.execute(
            "INSERT INTO holiday_countdown (holiday, days_left, timestamp) VALUES (%s, %s, %s)",
            ("Jouluun", days_until(christmas_date), timestamp),
        )

    if midsummer_date:
        cursor.execute(
            "INSERT INTO holiday_countdown (holiday, days_left, timestamp) VALUES (%s, %s, %s)",
            ("Juhannukseen", days_until(midsummer_date), timestamp),
        )

    conn.commit()
    cursor.close()
    conn.close()

    print("Juhlapyhien countdown tallennettu.")

if __name__ == "__main__":
    main()
