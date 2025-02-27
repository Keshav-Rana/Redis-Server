import unittest
from services.RESPService import RESPService

class SET_tests(unittest.TestCase):
    def keyWithDoubleQuotes():
        input_cmd = 'SET "test" val'
        serialised_input = "*3\r\n$3\r\nSET\r\n$4\r\ntest\r\n$3\r\nval\r\n"
        response_from_redis = "+OK\r\n"
        response_displayed_to_user = "OK"

    def valueWithDoubleQuotes():
        input_cmd = 'SET test "val"'
        serialised_input = "*3\r\n$3\r\nSET\r\n$4\r\ntest\r\n$3\r\nval\r\n"
        response_from_redis = "+OK\r\n"
        response_displayed_to_user = "OK"

    def keyWithSingleQuotes():
        input_cmd = "SET 'test' val"
        serialised_input = "*3\r\n$3\r\nSET\r\n$4\r\ntest\r\n$3\r\nval\r\n"
        response_from_redis = "+OK\r\n"
        response_displayed_to_user = "OK"

    def valueWithSingleQuotes():
        input_cmd = "SET test 'val'"
        serialised_input = "*3\r\n$3\r\nSET\r\n$4\r\ntest\r\n$3\r\nval\r\n"
        response_from_redis = "+OK\r\n"
        response_displayed_to_user = "OK"

    def noKey():
        input_cmd = "SET val"
        serialised_input = "*2\r\n$3\r\nSET\r\n$3\r\nval\r\n"
        # assert error

    def noValue():
        input_cmd = "SET key"
        serialised_input = "*2\r\n$3\r\nSET\r\n$3\r\nkey\r\n"
        # assert error

    def noArguments():
        input_cmd = "SET"
        serialised_input = "*1\r\n$3\r\nSET\r\n"
        # assert error