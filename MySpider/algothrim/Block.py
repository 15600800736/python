# encoding=UTF-8

class block:
    username = None
    content = None
    flag = None
    retweet = None
    range = None
    id = None

    def __init__(self):
        pass


    def toString(self):
        return self.username + "   :   " + self.content