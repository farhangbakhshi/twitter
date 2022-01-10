from database_handler import DatabaseHandler
from core import Core
from interface import Interface


db_handler = DatabaseHandler()
twitter_core = Core(db_handler)

twitter_interface = Interface(twitter_core)
twitter_interface.welcome()