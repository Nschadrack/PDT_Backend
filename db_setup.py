import sqlite3

# Step 1: Establish connection to the database
conn = sqlite3.connect('pdt.db')

# Step 2: Creating tables
cursor = conn.cursor()
query = '''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT
    )
'''

cursor.execute(query)

query = '''
    CREATE TABLE IF NOT EXISTS sessions(
    id INTEGER PRIMARY KEY,
    email TEXT,
    logged_in INT
    )
'''

cursor.execute(query)

conn.commit()

# Step 5: Close the connection
conn.close()
