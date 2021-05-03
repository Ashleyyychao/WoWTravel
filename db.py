import sqlite3 as sql

class DatebaseDriver(object):
    def __init__(self):
        # Sharing a single SQLite connection in multiple threads 
        self.con = sql.connect('database.db', check_same_thread = False)
        print('Opened database successfully')
        self.create_table()
    
    def create_table(self):
        try:
            self.con.execute(
                """
                CREATE TABLE member (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    birthday INTEGER NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL
                );
                """
            )
            print('Table created successfully')
        except Exception as e:
            print(e)

    def get_all_members(self):
        cursor = self.con.execute(
            "SELECT * FROM member;"
        )
        members = []
        for row in cursor:
            members.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "password": row[3],
                "birthday": row[4],
                "age": row[5],
                "gender": row[6]
            })
        return members

    def insert_member_table(self, name, email, password, birthday, age, gender):
        cursor = self.con.execute(
            """
            INSERT INTO member(name, email, password, birthday, age, gender) 
            VALUES(?, ?, ?, ?, ?, ?);
            """, (name, email, password, birthday, age, gender))
        self.con.commit()
        # 回傳最後一筆id
        return cursor.lastrowid

    def get_member_by_id(self, id):
        cursor = self.con.execute(
            """
            SELECT * FROM member 
            WHERE id = ?;
            """,(id,)
        )
        for row in cursor:
            return row
        return None

    def is_member(self, email):
        cursor = self.con.execute(
            """
            SELECT * FROM member 
            WHERE email = ?;
            """,(email,)
        )
        for row in cursor:
            return True
        return False

    def get_member_name_by_login(self, email, password):
        cursor = self.con.execute(
            """
            SELECT name FROM member 
            WHERE email = ? AND password = ?;
            """,(email, password)
        )
        for row in cursor:
            return row[0]
        return None

    # 改密碼
    def update_member_password_by_login(self, new_password, email, old_password):
        cursor = self.con.execute(
            """
            UPDATE member 
            SET password = ?
            WHERE email = ? AND password = ?;
            """,(new_password, email, old_password)
        )
        self.con.commit()