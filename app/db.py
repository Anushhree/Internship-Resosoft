import sqlite3

DB_PATH = r"C:\Users\Anushree\public_holiday\app\database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public_holidays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country_code TEXT NOT NULL,
        year INTEGER NOT NULL,
        date TEXT NOT NULL,
        local_name TEXT,
        name TEXT,
        fixed BOOLEAN,
        global BOOLEAN,
        counties TEXT,
        launch_year INTEGER,
        type TEXT
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized and table created (if not already).")