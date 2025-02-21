import unittest
from services.RESPService import RESPService

class ECHO_tests(unittest.TestCase):
    def messageInDoubleQuotes():
        input_cmd = 'ECHO "hello world"'
        serialised_input = "$4\r\nECHO\r\n$11\r\nhello world\r\n"
        response_from_redis = "$11\r\nhello world\r\n"
        response_displayed_to_user = '"hello world"'

    def messageInSingleQuotes():
        input_cmd = "ECHO 'testing 121'"
        serialised_input = "$4\r\nECHO\r\n$11\r\ntesting 121\r\n"
        response_from_redis = "$11\r\nhello world\r\n"
        response_displayed_to_user = '"hello world'

    def messagewithNoQuotes():
        input_cmd = "ECHO testing12345"
        serialised_input = "$4\r\nECHO\r\n$12\r\n\testing12345\r\n"
        response_from_redis = "$12\r\ntesting12345\r\n"
        response_dispayed_to_user = '"testing12345"'

    def invalidMessage():
        input_cmd = "ECHO test '2'"
        serialised_input = "$4\r\nECHO\r\n$4\r\ntest\r\n$1\r\n2\r\n"
        # check if exception was thrown

    def emptyString():
        input_cmd = "ECHO ''"
        input_cmd_two = 'ECHO ""'
        serialised_input = "$4\r\nECHO\r\n$0\r\n\r\n"
        response_from_redis = "$0\r\n\r\n"