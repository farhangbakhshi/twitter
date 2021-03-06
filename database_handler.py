import sqlite3
from sqlite3 import Error
import time


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
                username TEXT UNIQUE,
                password TEXT,
                name TEXT,
                bio TEXT
            )
            """
        )

        self.db_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tweets(
                id INTEGER PRIMARY KEY,
                author_id INTEGER,
                replying_to INTEGER,
                txt TEXT,
                time REAL,
                FOREIGN KEY (author_id) REFERENCES user(id),
                FOREIGN KEY (replying_to) REFERENCES tweets(id)
            )
            """
        )

        self.db_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS follows(
                id INTEGER PRIMARY KEY,
                follower_id INTEGER,
                followee_id INTEGER,
                FOREIGN KEY (follower_id) REFERENCES user(id),
                FOREIGN KEY (followee_id) REFERENCES user(id)
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

    def new_tweet(self, author_id, text):
        try:
            self.db_cursor.execute(
                """INSERT INTO tweets VALUES (:id, :author_id, :replying_to, :txt, :time)""",
                {
                    "id": None,
                    "author_id": author_id,
                    "replying_to": None,
                    "txt": text,
                    "time": time.time(),
                },
            )
            self.db_conn.commit()
            return True
        except Error:
            print(Error)
            return False

    def query(self, table_name, key_name, value):
        self.db_cursor.execute(f"SELECT * FROM {table_name} WHERE {key_name} = {value}")
        return self.db_cursor.fetchall()

    def search_usernames(self, s_phrase):
        self.db_cursor.execute(
            f"SELECT username,name,bio FROM users WHERE username LIKE '%{s_phrase}%'"
        )
        return self.db_cursor.fetchall()

    def search_tweets(self, s_phrase):
        self.db_cursor.execute(
            f"SELECT author_id,txt,time FROM tweets WHERE txt LIKE '%{s_phrase}%'"
        )
        return self.db_cursor.fetchall()

    def follow_by_username(self, follower, followee):
        try:
            self.db_cursor.execute(
                "INSERT INTO follows VALUES (:id, :follower_id, :followee_id)",
                {"id": None, "follower_id": follower, "followee_id": followee},
            )
            self.db_conn.commit()
            return True
        except Error:
            print(Error)
            return False

    def unfollow_by_username(self, unfollower_id, unfollowee_id):
        try:
            self.db_cursor.execute(
                f"DELETE FROM follows WHERE follower_id = {unfollower_id} AND followee_id = {unfollowee_id}"
            )
            self.db_conn.commit()
            return True
        except Error:
            print(Error)
            return False

    def get_last_10_tweets(self, user_id):
        self.db_cursor.execute(
            f"SELECT * FROM tweets WHERE author_id = {user_id} LIMIT 10"
        )
        return self.db_cursor.fetchmany(10)
