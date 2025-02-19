import re

class CommandService:
    def __init__(self, message):
        self.operation = message[2]
        self.message = message
    
    def makeResponse(self):
        if self.operation == "PING":
            return "+PONG\r\n"
        
        elif self.operation == "ECHO":
            response = ""
            sum = 0
            # start from 2nd element to fetch echo strings size
            if (len(self.message) >= 4):
                for i in range(3, len(self.message), 2):
                    # pattern $ followed by some digits
                    match = re.search(r'\$(\d+)', self.message[i])
                    if match:
                        sum += int(match.group(1)) # capture the digits from the string

            response += "$" + str(sum) + "\r\n"

            # start from 3rd element onwards to fetch the echo strings
            if (len(self.message) >= 5):
                for i in range(4, len(self.message), 2):
                    response += self.message[i] + " "
                    
            return response
        
        else:
            return "+Error\r\n"