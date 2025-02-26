import re
from services.Redis import Redis
class CommandService:
    def __init__(self, message, db):
        self.operation = message[2]
        self.message = message
        self.db = db
    
    def makeResponse(self):
        if self.operation == "PING":
            return "+PONG\r\n"
        
        elif self.operation == "ECHO":
            # validate arguments
            if (len(self.message) > 6):
                raise Exception("Invalid arguments. There can be only 1 argument")
            
            return self.message[3] + "\r\n" +  self.message[4] + "\r\n"
        
        elif self.operation == "SET":
            # validate arguments
            if (len(self.message) != 8):
                raise Exception("Invalid arguments. There should be 2 arguments")
            
            # insert key val in redis db
            self.db.set(self.message[4], self.message[6])
            
            return "+OK\r\n"


        elif self.operation == "GET":
            # validate arguments
            if (len(self.message) > 6):
                raise Exception("Invalid arguments. There can be only 1 argument")
            
            # get the length of value of key
            valLen = len(self.db.get(self.message[4]))
            val = self.db.get(self.message[4])

            return f"${valLen}\r\n{val}\r\n"

        elif self.operation == "EXPIRE":
            pass
        
        else:
            return "+Error\r\n"