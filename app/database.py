import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "biodata.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS biodata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date_of_birth TEXT,
            time_of_birth TEXT,
            education TEXT,
            address TEXT,
            mobile_numbers TEXT,
            email_addresses TEXT     
        )
    """)
    # Ensure new columns exist for older databases
    cursor.execute("PRAGMA table_info(biodata)")
    existing_cols = [row[1] for row in cursor.fetchall()]
    if 'mobile_numbers' not in existing_cols:
        cursor.execute("ALTER TABLE biodata ADD COLUMN mobile_numbers TEXT")
    if 'email_addresses' not in existing_cols:
        cursor.execute("ALTER TABLE biodata ADD COLUMN email_addresses TEXT")
    conn.commit()
    conn.close()