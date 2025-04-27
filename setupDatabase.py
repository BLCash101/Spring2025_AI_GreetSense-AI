import sqlite3

# Connect (or create if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
''')

# Create log table (to record entry/exit)
cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    timestamp TEXT,
    event_type TEXT  -- 'entry' or 'exit'
)
''')

conn.commit()
conn.close()

print("Database and tables created successfully.")

import os
print("Current working directory:", os.getcwd())
print("File created:", os.path.isfile('database.db'))
