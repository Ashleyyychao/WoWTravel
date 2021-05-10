import sqlite3 as sql


class DatebaseDriver(object):
    def __init__(self):
        # Sharing a single SQLite connection in multiple threads
        self.con = sql.connect('database.db', check_same_thread=False)
        print('Opened database successfully')
        self.create_table()
        self.create_messenger()

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
        # return cursor.fetchall()

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
            """, (id,)
        )
        return cursor.fetchone()

    def get_member_by_login(self, email, password):
        # Email是否註冊過
        cursor = self.con.execute(
            """
            SELECT * FROM member 
            WHERE email = ?;
            """, (email,)
        )
        # 是否登入成功
        for row in cursor:
            cursor = self.con.execute(
                """
                SELECT * FROM member
                WHERE email = ? AND password = ?;
                """, (email, password)
            )

            return True, cursor.fetchone()
        return False, cursor.fetchone()

    # 改密碼
    def update_member_password_by_login(self, new_password, email, old_password):
        cursor = self.con.execute(
            """
            UPDATE member SET password = ?
            WHERE email = ? AND password = ?;
            """, (new_password, email, old_password)
        )
        self.con.commit()
        return cursor.rowcount

    # 留言版

    def create_messenger(self):
        try:
            self.con.execute(
                """
                CREATE TABLE messenger(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    comment TEXT NOT NULL,
                    messenger_name TEXT NOT NULL
                );
                """
            )
            print('Table created successfully')
        except Exception as e:
            print(e)

    def insert_messenger_table(self, comment, messenger_name):
        cursor = self.con.execute(
            """
            INSERT INTO messenger(comment,messenger_name) 
            VALUES(?,?);
            """, (comment, messenger_name))
        self.con.commit()
        return cursor.lastrowid

    def get_messenger_by_id(self, id):
        cursor = self.con.execute(
            """
            SELECT * FROM messenger 
            WHERE id = ?;
            """, (id,)
        )
        for row in cursor:
            return row
        return None

    def get_all_messenger(self):
        cursor = self.con.execute(
            "SELECT * FROM messenger ORDER BY id DESC;"
        )
        messenger = []
        for row in cursor:
            messenger.append({
                "id": row[0],
                "comment": row[1],
                "messenger_name": row[2]
            })
        return messenger

    def update_messenger_by_id(self, id, comment, messenger_name):
        self.conn.execute(
            """
            UPDATE messenger
            SET comment = ? ,messenger_name = ?
            WHERE id = ?;
            """,
            (comment, messenger_name, id)
        )
        self.conn.commit()

    def delete_messenger_by_id(self, id):

        self.conn.execute(
            """
            DELETE FROM messenger
            WHERE id = ?;
            """,
            (id,),
        )
        self.conn.commit()
