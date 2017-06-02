# encoding=UTF-8

class block:
    username = None
    content = None
    side = None
    
    def toString(self):
        return self.username + "   :   " + self.content