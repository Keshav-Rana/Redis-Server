class CommandService:
    def __init__(self, message):
        self.operation = message[2]
    
    def makeResponse(self):
        if self.operation == "PING":
            return "+PONG\r\n"