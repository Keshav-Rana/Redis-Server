import unittest
from services.RESPService import RESPService

class ECHO_tests(unittest.TestCase):
    def basicTest():
        input_cmd = 'ECHO "hello world"'
        response_from_redis = "$11\r\nhello world\r\n"
        response_displayed_to_user = '"hello world"'

    def edgeCaseOneTest():
        pass

    def edgeCaseTwoTest():
        pass