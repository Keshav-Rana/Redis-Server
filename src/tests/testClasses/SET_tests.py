import unittest
from services.RESPService import RESPService

class SET_tests(unittest.TestCase):
    def keyWithDoubleQuotes():
        input_cmd = 'SET "test" val'
        serialised_input = "*3\r\n$3\r\nSET\r\n$4\r\ntest\r\n$3\r\nval\r\n"
        response_from_redis = ""

    def valueWithDoubleQuotes():
        pass

    def keyWithSingleQuotes():
        pass

    def valueWithSingleQuotes():
        pass

    def normalKey():
        pass

    def normalValue():
        pass

    def noKey():
        pass

    def noValue():
        pass

    def noArguments():
        pass