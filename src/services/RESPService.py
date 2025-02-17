class RESPService:
    @staticmethod
    def serialiser(input_cmd):
        # split the input command by spaces and get the operation
        operation = input_cmd.split()[0]
    
    @staticmethod
    def deserialiser(redis_response):
        pass