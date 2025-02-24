import re

class CommandService:
    def __init__(self, message):
        self.operation = message[2]
        self.message = message
    
    def makeResponse(self):
        if self.operation == "PING":
            return "+PONG\r\n"
        
        elif self.operation == "ECHO":
            # validate arguments
            if (len(self.message) > 6):
                raise Exception("Invalid arguments. There can be only 1 argument")
            
            return self.message[3] + "\r\n" +  self.message[4] + "\r\n"
        
        elif self.operation == "SET":
            pass

        elif self.operation == "GET":
            pass

        elif self.operation == "EXPIRE":
            pass
        
        else:
            return "+Error\r\n"