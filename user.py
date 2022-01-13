class User:
    id = None
    username = None
    password = None
    name = None
    bio = None

    def __init__(self, username, password, name, bio):
        self.username = username
        self.password = password
        self.name = name
        self.bio = bio
