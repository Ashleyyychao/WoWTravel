import sqlite3 as sql
con = sql.connect('database.db')
print('Opened database successfully')

con.execute(
    """
    CREATE TABLE member (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        birthday INTEGER NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL
    )
    """
)
print('Table created successfully')
con.close()