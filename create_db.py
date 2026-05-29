import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bruger_id TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users (bruger_id, password)
VALUES (?, ?)
""", ("coop123", "test123"))

conn.commit()
conn.close()

print("Database created")