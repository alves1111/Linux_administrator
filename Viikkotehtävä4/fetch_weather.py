#!/usr/bin/env python3
import os
import requests
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv

# Lataa .env-tiedoston muuttujat
load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")
CITY = os.getenv("CITY", "Helsinki")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "weather_db")

URL = (
    "https://api.openweathermap.org/data/2.5/weather"
    f"?q={CITY}&appid={API_KEY}&units=metric"
)

def main():
    # Yhdistetään tietokantaan
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # Luodaan taulu, jos sitä ei ole
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city VARCHAR(50),
            temperature FLOAT,
            description VARCHAR(100),
            timestamp DATETIME
        )
        """
    )

    # Haetaan data API:sta
    resp = requests.get(URL, timeout=10)
    data = resp.json()

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    timestamp = datetime.now()

    # Tallennetaan tietokantaan
    cursor.execute(
        """
        INSERT INTO weather_data (city, temperature, description, timestamp)
        VALUES (%s, %s, %s, %s)
        """,
        (CITY, temp, desc, timestamp),
    )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Data tallennettu: {CITY} {temp}°C {desc} @ {timestamp}")

if __name__ == "__main__":
    main()
