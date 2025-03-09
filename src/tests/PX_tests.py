import unittest
import time

from services.RESPService import RESPService
from services.CommandService import CommandService
from services.Redis import Redis

class PX_tests(unittest.TestCase):
    def setUp(self):
        self.resp = RESPService()
        self.redis_db = Redis()

    def test_hundredMilliseconds(self):
        input_cmd = "SET hundred 100 PX 100"
        serialised_input = "*5\r\n$3\r\nSET\r\n$7\r\nhundred\r\n$3\r\n100\r\n$2\r\nPX\r\n$3\r\n100\r\n"
        self.assertEqual(self.resp.serialiser(input_cmd), serialised_input)

        response_from_redis = "+OK\r\n"
        # split serialised data
        splitted_data = self.resp.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "OK"
        self.assertEqual(self.resp.deserialiser(splitted_data[2], response), response_displayed_to_user)

        # check if the key exists
        self.assertEqual(self.redis_db.get("hundred"), '100')

        # wait 200 milliseconds and check if the key has expired
        time.sleep(0.2)
        self.assertEqual(self.redis_db.get("hundred"), None)

    def test_zeroMilliseconds(self): 
        input_cmd = "SET zero 0 PX 0"
        serialised_input = "*5\r\n$3\r\nSET\r\n$4\r\nzero\r\n$1\r\n0\r\n$2\r\nPX\r\n$1\r\n0\r\n"
        self.assertEqual(self.resp.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR invalid expire time in 'set' command\r\n"
        # split serialised data
        splitted_data = self.resp.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR invalid expire time in 'set' command"
        self.assertEqual(self.resp.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_negativeMilliseconds(self):
        input_cmd = "SET negative -1 PX -100"
        serialised_input = "*5\r\n$3\r\nSET\r\n$8\r\nnegative\r\n$2\r\n-1\r\n$2\r\nPX\r\n$4\r\n-100\r\n"
        self.assertEqual(self.resp.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR invalid expire time in 'set' command\r\n"
        # split serialised data
        splitted_data = self.resp.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR invalid expire time in 'set' command"
        self.assertEqual(self.resp.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_invalidInput(self):
        input_cmd = "SET invalid inv PX invalid"
        serialised_input = "*5\r\n$3\r\nSET\r\n$7\r\ninvalid\r\n$3\r\ninv\r\n$2\r\nPX\r\n$7\r\ninvalid\r\n"
        self.assertEqual(self.resp.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR value is not an integer or out of range\r\n"
        # split serialised data
        splitted_data = self.resp.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR value is not an integer or out of range"
        self.assertEqual(self.resp.deserialiser(splitted_data[2], response), response_displayed_to_user)

if __name__ == "__main__":
    unittest.main()