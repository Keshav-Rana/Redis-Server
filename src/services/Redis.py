import threading

# storage for redis
class Redis:
    def __init__(self):
        self.data = {}

    def set(self, key, value, option=None, time=None):
        self.data[key] = value

        # EX implementation
        if time is not None and option is not None:
            if (option == "EX"):
                timer = threading.Timer(int(time), self.delete, args=(key,))
                timer.start()
            elif option == "PX":
                timeInMilliseconds = int(time) / 1000
                print(timeInMilliseconds)
                timer = threading.Timer(timeInMilliseconds, self.delete, args=(key,))
                timer.start()
            elif option == "EAXT":
                pass
            elif option == "PXAT":
                pass

    def get(self, key):
        try:
            return self.data[key]
        except KeyError:
            return None
    
    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def keys(self):
        return list(self.data.keys)