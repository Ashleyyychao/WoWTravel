import sqlite3 as sql
con = sql.connect('database.db')
print('Opened database successfully')

con.execute(
    """
    CREATE TABLE account (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """
)
print('Table created successfully')
con.close()