import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE users
ADD COLUMN failed_attempts INTEGER DEFAULT 0
""")

cursor.execute("""
ALTER TABLE users
ADD COLUMN lock_until REAL DEFAULT 0
""")

conn.commit()
conn.close()

print("Database updated")