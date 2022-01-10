import sqlite3
from sqlite3 import Error


class DatabaseHandler:
    db_conn = None
    db_cursor = None

    def __init__(self):
        self.db_conn = self.make_conn()
        self.db_cursor = self.db_conn.cursor()

        self.db_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                username text UNIQUE,
                password text,
                name text,
                bio text
            )
            """
        )

        self.db_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tweets(
                id INTEGER PRIMARY KEY,
                author_id text,
                txt text
            )
            """
        )

        self.db_conn.commit()
    
    def make_conn(self):
        try:
            conn = sqlite3.connect("database.db")
            return conn
        except Error:
            print(Error)

    def close_conn(self):
        self.db_conn.commit()
        self.db_conn.close()

    def save_new_user(self, username, password, name, bio):
        try:
            self.db_cursor.execute(
                """INSERT INTO users VALUES (:id, :username, :password, :name, :bio)""",
                {
                    "id": None,
                    "username": username,
                    "password": password,
                    "name": name,
                    "bio": bio,
                },
            )
            self.db_conn.commit()
            return True
        except Error:
            return False



    def query(self, table_name, key_name, value):
        self.db_cursor.execute(
            "SELECT * FROM users WHERE username = :value", {"value": value}
        )
        return self.db_cursor.fetchall()