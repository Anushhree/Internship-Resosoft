import sqlite3

DB_NAME = "locations.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            place_name TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL
        )
    """)
    conn.commit()
    conn.close()

def get_coordinates_from_db(place_name: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude FROM locations WHERE place_name = ?", (place_name,))
    row = cursor.fetchone()
    conn.close()
    return row

def save_coordinates_to_db(place_name: str, latitude: float, longitude: float):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO locations (place_name, latitude, longitude) VALUES (?, ?, ?)",
                   (place_name, latitude, longitude))
    conn.commit()
    conn.close()