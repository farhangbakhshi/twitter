
from database_handler import DatabaseHandler


class Core:

    database_handler = None
    
    def __init__(self, db_handler:DatabaseHandler):
        self.database_handler = db_handler
    
    def wrap_up(self):
        self.database_handler.close_conn()


    def new_user(self, username, password, name, bio):
        return self.database_handler.save_new_user(username, password, name, bio)
        