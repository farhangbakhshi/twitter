import hashlib

class User:
    id = None
    username = None
    password = None
    name = None
    bio = None

    def __init__(self, username, password, name, bio):
        self.username = username
        encoded_password = password.encode()
        self.password = hashlib.sha256(encoded_password).hexdigest()
        self.name = name
        self.bio = bio
        