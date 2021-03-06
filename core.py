import hashlib
from user import User
from tweet import Tweet
from database_handler import DatabaseHandler


def key_function(tweet):
    """
    this function gets a contact and returns its name to be used in a sort function as the key to sort. SORT IS DONE IN GET_HOME()
    """
    return tweet[3]


class Core:

    database_handler = None

    def __init__(self, db_handler: DatabaseHandler):
        self.database_handler = db_handler

    def wrap_up(self):
        self.database_handler.close_conn()

    def new_user(self, username, password, name, bio):
        for x in username:
            if ord(x) > 64 and ord(x) < 91:
                continue
            elif ord(x) > 96 and ord(x) < 123:
                continue
            elif ord(x) > 47 and ord(x) < 58:
                continue
            elif ord(x) == 95:
                continue
            else:
                print(
                    "the username can only contain english letters, numbers, and underline."
                )
                return False

        encoded_password = password.encode()
        password = hashlib.sha256(encoded_password).hexdigest()
        return self.database_handler.save_new_user(username, password, name, bio)

    def check_login(self, username, password):
        # first we need the password to be comparable to the result we're going to get from the database
        encoded_password = password.encode()
        password = hashlib.sha256(encoded_password).hexdigest()

        result = self.database_handler.query("users", "username", f"'{username}'")
        if len(result) != 0 and result[0][2] == password:
            user: User = User(result[0][1], result[0][2], result[0][3], result[0][4])
            user.id = result[0][0]
            return user
        else:
            return None

    def new_tweet(self, author_id, text):
        return self.database_handler.new_tweet(author_id, text)

    def search_by_user(self, s_phrase):
        return self.database_handler.search_usernames(s_phrase)

    def search_by_tweet(self, s_phrase):
        result_list = self.database_handler.search_tweets(s_phrase)
        for x in range(len(result_list)):
            result_list[x] = list(result_list[x])
            result_list[x][0] = self.database_handler.query(
                "users", "id", result_list[x][0]
            )[0][1]
        return result_list

    def follow_by_username(self, follower_id, followee_username):
        result = self.database_handler.query(
            "users", "username", f"'{followee_username}'"
        )
        if result:
            followee_id = result[0][0]
        else:
            print("No such user found.")
            return False
        return self.database_handler.follow_by_username(follower_id, followee_id)

    def unfollow_by_username(self, unfollower_id, unfollowee_username):
        result = self.database_handler.query(
            "users", "username", f"'{unfollowee_username}'"
        )
        if result:
            unfollowee_id = result[0][0]
        else:
            print("No such user found.")
            return False
        return self.database_handler.unfollow_by_username(unfollower_id, unfollowee_id)

    def get_home(self, user_id):
        # preparing a list of followings by preparing a list of their IDs
        followings = self.database_handler.query("follows", "follower_id", user_id)
        for x in range(len(followings)):
            followings[x] = followings[x][2]
        # now we get a list of each user's last 10 tweets and then make a list of those lists
        tweets_list = []
        for x in followings:
            tweets_list.append(self.database_handler.get_last_10_tweets(x))
        # now we turn each of those tuples into a Tweet
        for x in range(len(tweets_list)):
            for y in range(len(tweets_list[x])):
                tweets_list[x][y] = Tweet(
                    tweets_list[x][y][0],
                    tweets_list[x][y][1],
                    tweets_list[x][y][2],
                    tweets_list[x][y][3],
                    tweets_list[x][y][4],
                )
        # now we prepare this list for home(we have to sort them by time)
        home = []
        for x in tweets_list:
            for y in x:
                home.append(
                    [
                        self.database_handler.query("users", "id", y.author_id)[0][1],
                        self.database_handler.query("users", "id", y.author_id)[0][3],
                        y.text,
                        y.time,
                    ]
                )
        home.sort(key=key_function, reverse=True)
        return home
