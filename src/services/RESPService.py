import re

class RESPService:
    @staticmethod
    def serialiser(input_cmd):
        # split the input command by spaces and get the operation
        message_list = input_cmd.split()
        message_size = len(message_list)

        final_message = f"*{message_size}"

        for message in message_list:
            final_message += f"\r\n${len(message)}\r\n{message}"

        return final_message
    
    @staticmethod
    def deserialiser(redis_response):
        # remove unwanted characters
        redis_response = redis_response.replace("+", "")
        redis_response = redis_response.replace("\r\n", "")
        redis_response = re.sub(r'\$\d+', '', redis_response)

        return redis_response