# encoding=UTF-8

class block:
    username = None
    content = None
    side = None
    retweed = None

    def __init__(self):
        pass

    # def __init__(self, username, content):
    #     self.username = username
    #     self.content = content

    def toString(self):
        return self.username + "   :   " + self.content