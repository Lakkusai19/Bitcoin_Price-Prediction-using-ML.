import sqlite3

# Connect to SQLite Database (it will create the db file if it doesn't exist)
conn = sqlite3.connect('btc_prices.db')
cursor = conn.cursor()

# 1. Create Table (if not exists)
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# 2. Insert Data (Create)
cursor.execute('''
INSERT INTO user (username, email, password) 
VALUES (?, ?, ?)
''', ('john_doe', 'john.doe@example.com', 'password123'))

conn.commit()

# 3. Read Data (Select)
cursor.execute('SELECT * FROM user')
rows = cursor.fetchall()
print("Users:")
for row in rows:
    print(row)

# 4. Update Data
cursor.execute('''
UPDATE user
SET email = ?
WHERE username = ?
''', ('john.doe@newdomain.com', 'john_doe'))

conn.commit()

# 5. Delete Data
cursor.execute('''
DELETE FROM user
WHERE username = ?
''', ('john_doe',))

conn.commit()

# Close the connection
conn.close()
