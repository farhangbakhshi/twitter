import hashlib
from user import User
from database_handler import DatabaseHandler


class Core:

    database_handler = None
    
    def __init__(self, db_handler:DatabaseHandler):
        self.database_handler = db_handler
    
    def wrap_up(self):
        self.database_handler.close_conn()


    def new_user(self, username, password, name, bio):
        encoded_password = password.encode()
        password = hashlib.sha256(encoded_password).hexdigest()
        return self.database_handler.save_new_user(username, password, name, bio)

    def check_login(self, username, password):
        #first we need the password to be comparable to the result we're going to get from the database
        encoded_password = password.encode()
        password = hashlib.sha256(encoded_password).hexdigest()

        result = self.database_handler.query("users", "username", f"'{username}'")
        if len(result) !=0 and result[0][2] == password:
            user:User = User(result[0][1], result[0][2], result[0][3], result[0][4])
            user.id = result[0][0]
            return user
        else:
            return None
        