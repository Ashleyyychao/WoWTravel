import sqlite3 as sql


class DatebaseDriver(object):
    def __init__(self):
        # Sharing a single SQLite connection in multiple threads
        self.con = sql.connect('database.db', check_same_thread=False)
        print('Opened database successfully')
        self.create_table()
        self.create_message()

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
    def create_message(self):
        try:
            self.con.execute(
                """
                CREATE TABLE message(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    comment TEXT NOT NULL,
                    member_id INTEGER NOT NULL,
                    FOREIGN KEY (member_id) REFERENCES member(id)
                );
                """
            )
            print('Table created successfully')
        except Exception as e:
            print(e)

    def insert_message_table(self, email, comment, member_id):
        cursor = self.con.execute(
            """
            INSERT INTO message(email, comment, member_id) 
            VALUES(?,?,?);
            """, (email, comment, member_id))
        self.con.commit()
        return cursor.lastrowid

    def get_message_by_id(self, id):
        cursor = self.con.execute(
            """
            SELECT * FROM message 
            WHERE id = ?;
            """, (id,)
        )
        for row in cursor:
            return row
        return None

    def get_all_messages(self):
        cursor = self.con.execute(
            "SELECT * FROM message ORDER BY id DESC;"
        )
        message = []
        for row in cursor:
            message.append({
                "id": row[0],
                "email": row[1],
                "comment": row[2]
            })
        return message

    # page:第幾頁 n:一頁幾筆
    def get_message_by_page(self, page, n):
        cursor = self.con.execute(
            """
            SELECT * FROM message
            ORDER BY id DESC
            LIMIT ?, ?;
            """, (page, n)
        )
        message = []
        for row in cursor:
            message.append({
                "id": row[0],
                "email": row[1],
                "comment": row[2]
            })
        return message

    def update_message_by_id(self, id, email, comment):
        self.con.execute(
            """
            UPDATE message
            SET email = ?, comment = ? 
            WHERE id = ?;
            """,
            (email, comment, id)
        )
        self.con.commit()

    def delete_message_by_id(self, id):

        self.con.execute(
            """
            DELETE FROM message
            WHERE id = ?;
            """,
            (id,)
        )
        self.con.commit()
