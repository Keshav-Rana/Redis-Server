# storage for redis

class Redis:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data[key]
    
    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def keys(self):
        return list(self.data.keys)