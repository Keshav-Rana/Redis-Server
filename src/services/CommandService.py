class CommandService:
    def __init__(self, message):
        self.operation = message[2]
        self.message = message
    
    def makeResponse(self):
        if self.operation == "PING":
            return "+PONG\r\n"
        
        elif self.operation == "ECHO":
            response = ""
            # start from 3rd element onwards
            if (len(self.message) >= 5):
                for i in range(4, len(self.message), 2):
                    response += self.message[i] + " "
                    
            return response
        
        else:
            return "+Error\r\n"