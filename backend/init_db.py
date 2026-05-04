import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT
)
""")

# INSERT SAMPLE USER
cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
               ("admin@gmail.com", "1234"))

conn.commit()
conn.close()

print("Database created!")
