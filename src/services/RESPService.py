import re

class RESPService:
    @staticmethod
    def serialiser(input_cmd):
        # find double quotes, single quotes and sequence on non whitespace chars
        pattern = r'\".*?\"|\'.*?\'|\S+'
        matches = re.findall(pattern, input_cmd)
        elements = [match.strip('"').strip("'") for match in matches]

        message = f"*{len(elements)}\r\n"

        # create RESP message
        for element in elements:
            message += f"${len(element)}\r\n"
            message += f"{element}\r\n"

        return message
    
    @staticmethod
    def deserialiser(cmd, redis_response):
        if (cmd == "ECHO"):
            lines = redis_response.split('\r\n')

            # check if it's bulk string
            if lines[0].startswith("$"):
                length = int(lines[0][1:])
                content = lines[1]
                if length == len(content):
                    return content