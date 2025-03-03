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
                return "-ERR wrong number of arguments for 'echo' command\r\n"
            
            return self.message[3] + "\r\n" +  self.message[4] + "\r\n"
        
        elif self.operation == "SET":
            # validate arguments
            if (len(self.message) != 8):
                return "-ERR wrong number of arguments for 'set' command\r\n"
            
            # insert key val in redis db
            self.db.set(self.message[4], self.message[6])
            
            return "+OK\r\n"


        elif self.operation == "GET":
            # validate arguments
            if (len(self.message) != 6):
                return "-ERR wrong number of arguments for 'get' command\r\n"
            
            val = self.db.get(self.message[4])

            # handle case where key does not exist
            if val == None:
                return "$-1\r\n"
            
            # get the length of value of key
            valLen = len(self.db.get(self.message[4]))

            return f"${valLen}\r\n{val}\r\n"
        
        elif self.operation == "CONFIG":
            # Handle CONFIG GET command
            if len(self.message) >= 6 and self.message[4].upper() == "GET":
                # Return mock configuration values
                if self.message[5].lower() == "save":
                    return "*2\r\n$4\r\nsave\r\n$3\r\n600\r\n"
                elif self.message[5].lower() == "appendonly":
                    return "*2\r\n$10\r\nappendonly\r\n$2\r\nno\r\n"
            
            return "-ERR unsupported CONFIG subcommand or wrong number of arguments\r\n"
        

        elif self.operation == "EXPIRE":
            pass
        
        else:
            return "+Error\r\n"