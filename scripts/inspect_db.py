import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / 'biodata.db'
print('DB path:', DB)
if not DB.exists():
    print('DB does not exist')
else:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(biodata)")
        cols = cur.fetchall()
        for c in cols:
            print(c)
    except Exception as e:
        print('Error:', e)
    finally:
        conn.close()
