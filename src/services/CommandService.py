import re
from services.Redis import Redis
from datetime import datetime, timezone

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
            if (len(self.message) < 8):
                return "-ERR wrong number of arguments for 'set' command\r\n"
            
            # check option EX
            if (len(self.message) > 8):
                if (self.message[8] == "EX"):
                    # check if the value is an integer
                    try:
                        timeInSeconds = int(self.message[10])
                        if (timeInSeconds <= 0):
                            return "-ERR invalid expire time in 'set' command\r\n"
                        
                        # insert key val in redis db and remove after timeInSeconds
                        self.db.set(self.message[4], self.message[6], self.message[8], self.message[10])
                    except ValueError:
                        return "-ERR value is not an integer or out of range\r\n"
                elif (self.message[8] == "PX"):
                    try:
                        timeInMilliseconds = int(self.message[10])
                        if (timeInMilliseconds <= 0):
                            return "-ERR invalid expire time in 'set' command\r\n"
                        
                        # insert key val in redis db and remove after timeInMilliseconds
                        self.db.set(self.message[4], self.message[6], self.message[8], self.message[10])
                    except ValueError:
                        return "-ERR value is not an integer or out of range\r\n"
                # unix time in seconds
                elif (self.message[8] == "EAXT"):
                    try:
                        unixTimeInSeconds = float(self.message[10])
                        # convert unix time to datetime obj
                        userDt = datetime.fromtimestamp(unixTimeInSeconds, tz=timezone.utc)
                        currDt = datetime.now(timezone.utc)

                        # calculate total seconds
                        totalSeconds = (userDt - currDt).total_seconds()

                        if (totalSeconds <= 0):
                            return "-ERR invalid expire time in 'set' command\r\n"

                        # insert key val in redis db and remove after time
                        self.db.set(self.message[4], self.message[6], self.message[8], totalSeconds)
                    except ValueError:
                        return "-ERR value is not an integer or out of range\r\n"
                # unix time in milliseconds
                elif self.message[8] == "PXAT":
                    try:
                        unixTimeInMilliseconds = float(self.message[10])
                        # convert unix time to datetime obj
                        userDt = datetime.fromtimestamp(unixTimeInMilliseconds, tz=timezone.utc)
                        currDt = datetime.now(timezone.utc)
                        
                        # calculate total seconds and convert to milliseconds
                        totalMilliseconds = ((userDt - currDt).total_seconds()) * 1000

                        if (totalMilliseconds <= 0):
                            return "-ERR invalid expire time in 'set' command\r\n"

                        # insert into redis db
                        self.db.set(self.message[4], self.message[6], self.message[8], totalMilliseconds)
                    except ValueError:
                        return "-ERR value is not an integer or out of range\r\n"
            
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
        
        elif self.operation == "EXISTS":
            # validate arguments
            if (len(self.message) <= 4):
                return "-ERR wrong number of arguments for 'exists' command\r\n"
            
            numOfKeys = 0
            
            # retrieve keys and check if each of them exists in db
            for i in range(4, len(self.message), 2):
                if self.db.get(self.message[i]) != None:
                    numOfKeys += 1

            return f":{numOfKeys}\r\n"
        
        elif self.operation == "DEL":
            # validate arguments
            if (len(self.message) <= 4):
                return "-ERR wrong number of arguments for 'exists' command\r\n"
            
            numOfKeys = 0
            
            # retrieve keys and check if each of them exists in db
            for i in range(4, len(self.message), 2):
                if self.db.get(self.message[i]) != None:
                    numOfKeys += 1
                    # delete key val
                    self.db.delete(self.message[i])

            return f":{numOfKeys}\r\n"

        elif self.operation == "INCR":
            # validate arguments
            if (len(self.message) <= 4 or len(self.message) > 6):
                return "-ERR wrong number of arguments for 'incr' command\r\n"
            
            # validate that the corresponding value of the key is convertible to integer
            try:
                key = self.message[4]
                val = int(self.db.get(key))
                # increment value
                val += 1
                self.db.set(key, str(val))
                return f":{str(val)}\r\n"
            except ValueError:
                return "-ERR value is not an integer or out of range\r\n"
            except TypeError:
                # case - key does not exist, straightway initialise it to 1 instead of first setting to 0 then incrementing
                self.db.set(self.message[4], "1")
                return ":1\r\n"

        elif self.operation == "DECR":
            # validate arguments
            if (len(self.message) <= 4 or len(self.message) > 6):
                return "-ERR wrong number of arguments for 'decr' command\r\n"
            
            # validate that the corresponding value of the key is convertible to integer
            try:
                key = self.message[4]
                val = int(self.db.get(key))
                # increment value
                val -= 1
                self.db.set(key, str(val))
                return f":{str(val)}\r\n"
            except ValueError:
                return "-ERR value is not an integer or out of range\r\n"
            except TypeError:
                # case - key does not exist, straightway initialise it to -1 instead of first setting to 0 then decrementing
                self.db.set(self.message[4], "-1")
                return ":-1\r\n"
        
        elif self.operation == "LPUSH":
            # validate arguments
            if not len(self.message) >= 7:
                return "-ERR wrong number of arguments for 'lpush' command\r\n"
            
            key = self.message[4]
            
            curr_list = self.db.get(key)
            if curr_list is None:
                curr_list = []
                self.db.set(key, curr_list)

            # validate it's a list
            if not isinstance(curr_list, list):
                return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value\r\n"
            
            # insert at head
            # for i in range(len(self.message)-2, 5, -2):
            #     curr_list.insert(0, self.message[i])

            for i in range(6, len(self.message), 2):
                curr_list.insert(0, self.message[i])

            # set the new list in db
            self.db.set(key, curr_list)

            return f":{len(curr_list)}\r\n"
            
        elif self.operation == "RPUSH":
            # validate arguments
            if not len(self.message) >= 7:
                return "-ERR wrong number of arguments for 'rpush' command\r\n"
            
            key = self.message[4]
            
            curr_list = self.db.get(key)
            if curr_list is None:
                curr_list = []
                self.db.set(key, curr_list)

            # validate it's a list
            if not isinstance(curr_list, list):
                return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value\r\n"
            
            # insert at tail
            for i in range(6, len(self.message), 2):
                curr_list.append(self.message[i])

            # set the new list in db
            self.db.set(key, curr_list)

            return f":{len(curr_list)}\r\n"

        # AOF mechanism
        elif self.operation == "SAVE":
            pass
        
        else:
            response = f"-ERR unknown command {self.message[2]}, with args beginning with: "
            for i in range(4, len(self.message), 2):
                response += f"'{self.message[i]}' "

            response += "\r\n"
            return response
