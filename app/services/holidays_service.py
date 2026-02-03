import requests
import sqlite3
from app.config import NAGER_DATE_API

DB_PATH = r"C:\Users\Anushree\public_holiday\app\database.db"

def fetch_holidays(country_code: str, year: int):
    url = f"{NAGER_DATE_API}/{year}/{country_code}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch holidays: {response.text}")

    holidays = response.json()
    save_holidays_to_db(country_code, year, holidays)
    return holidays

def save_holidays_to_db(country_code: str, year: int, holidays: list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for holiday in holidays:
        cursor.execute("""
            INSERT INTO public_holidays (
                country_code, year, date, local_name, name,
                fixed, global, counties, launch_year, type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            country_code,
            year,
            holiday.get("date"),
            holiday.get("localName"),
            holiday.get("name"),
            holiday.get("fixed"),
            holiday.get("global"),
            ",".join(holiday.get("counties") or []) if holiday.get("counties") else None,
            holiday.get("launchYear"),
            holiday.get("type")
        ))

    conn.commit()
    conn.close()