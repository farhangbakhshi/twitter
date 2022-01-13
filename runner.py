from database_handler import DatabaseHandler
from core import Core
import time

#-----------------------------------------------------------------------------------------------------
import argparse

parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

register = subparser.add_parser('register')
register.add_argument("--username", type=str, required=True)
register.add_argument("--password", type=str, required=True)
register.add_argument("--name", type=str, required=True)
register.add_argument("--bio", type=str, required=False)

login = subparser.add_parser('login')
login.add_argument("--username", type=str, required=True)
login.add_argument("--password", type=str, required=True)

login.add_argument('--tweet', type=str, required=False)
login.add_argument('--search-by-user', type=str, required=False)
login.add_argument('--search-by-tweet', type=str, required=False)
login.add_argument('--follow', type=str, required=False)
login.add_argument('--unfollow', type=str, required=False)
login.add_argument('--show-home', action='store_true', required=False)


args = parser.parse_args()
#-----------------------------------------------------------------------------------------------------

db_handler = DatabaseHandler()
twitter_core = Core(db_handler)

if args.command == "register":
    if twitter_core.new_user(args.username, args.password, args.name, args.bio):
        print("Done!")
    else:
        print("Register failed.")

if args.command == "login":
    user = twitter_core.check_login(args.username, args.password)
    if user:
        print("Logged in successfully.")
        #tweet
        if args.tweet:
            if twitter_core.new_tweet(user.id, args.tweet):
                print("Successfully tweeted!")
            else:
                print("Tweet failed.")
        #search by user
        if args.search_by_user:
            result_list = twitter_core.search_by_user(args.search_by_user)
            for x in range(len(result_list)):
                print(x + 1)
                print(result_list[x][1])
                print("@" + result_list[x][0])
                print("bio: " + str(result_list[x][2]))
                print("--------------------------------------------------------------------------------")
        #search by tweet
        if args.search_by_tweet:
            result_list = twitter_core.search_by_tweet(args.search_by_tweet)
            for x in range(len(result_list)):
                print(x + 1)
                print("@" + result_list[x][0])
                print(result_list[x][1])
                print(time.ctime(result_list[x][2]))
                print("--------------------------------------------------------------------------------")
        #follow by username
        if args.follow:
            if twitter_core.follow_by_username(user.id, args.follow):
                print("Followed successfully!")
            else:
                print("Failed to follow.")
        #unfollow by username
        if args.unfollow:
            if twitter_core.unfollow_by_username(user.id, args.unfollow):
                print("Unfollowed successfully!")
            else:
                print("Failed to unfollow.")
        #show home
        if args.show_home:
            home = twitter_core.get_home(user.id)
            for x in range(len(home)):
                print(x + 1)
                print(home[x][1])
                print("@" + home[x][0])
                print(home[x][2])
                print(time.ctime(home[x][3]))
                print("--------------------------------------------------------------------------------")
            
    else:
        print("Login failed.")