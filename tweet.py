

class Tweet:
    id = None
    author_id = None
    text = None
    replying_to = None
    time:float = None

    def __init__(self, id, author_id, replying_to, text, time):
        self.id = id
        self.author_id = author_id
        self. text = text
        self.replying_to = replying_to
        self.time = time
        