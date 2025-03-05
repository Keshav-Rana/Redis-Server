import threading

# storage for redis
class Redis:
    def __init__(self):
        self.data = {}

    def set(self, key, value, ex=None):
        self.data[key] = value

        # EX implementation
        if ex is not None:
            # remove the key value after ex seconds
            timer = threading.Timer(int(ex), self.delete, args=(key,))
            timer.start()

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