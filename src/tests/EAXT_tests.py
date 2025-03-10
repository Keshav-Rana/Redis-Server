import unittest
from services.Redis import Redis
from services.CommandService import CommandService
from services.RESPService import RESPService
import time
from datetime import datetime, timedelta

class EAXT_tests(unittest.TestCase):
    def setUp(self):
        self.resp_service = RESPService()
        self.redis_db = Redis()

    def test_normalCase(self):
        dt = datetime.now()
        # add 10 seconds to current time
        dt = dt + timedelta(seconds=10)
        # convert dt to unix time
        unixTime = time.mktime(dt.timetuple())

        input_cmd = f"SET ten 10 EAXT {unixTime}"
        print("input_cmd:", input_cmd)
        serialised_input = f"*5\r\n$3\r\nSET\r\n$3\r\nten\r\n$2\r\n10\r\n$4\r\nEAXT\r\n${len(str(unixTime))}\r\n{unixTime}\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "+OK\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "OK"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

        # check if the key exists
        self.assertEqual(self.redis_db.get("ten"), "10")

        # wait 11 seconds and check if the key has expired
        time.sleep(11)
        self.assertEqual(self.redis_db.get("ten"), None)

    def test_zeroSeconds(self): 
        dt = datetime.now()
        # convert dt to unix time
        unixTime = time.mktime(dt.timetuple())

        input_cmd = f"SET zero 0 EAXT {unixTime}"
        serialised_input = f"*5\r\n$3\r\nSET\r\n$4\r\nzero\r\n$1\r\n0\r\n$4\r\nEAXT\r\n${len(str(unixTime))}\r\n{unixTime}\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR invalid expire time in 'set' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR invalid expire time in 'set' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_negativeSeconds(self):
        dt = datetime.now()
        # subtract 10 seconds to current time
        dt = dt + timedelta(0, -10)
        # convert dt to unix time
        unixTime = time.mktime(dt.timetuple())

        input_cmd = f"SET negative -1 EAXT {unixTime}"
        serialised_input = f"*5\r\n$3\r\nSET\r\n$8\r\nnegative\r\n$2\r\n-1\r\n$4\r\nEAXT\r\n${len(str(unixTime))}\r\n{unixTime}\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR invalid expire time in 'set' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR invalid expire time in 'set' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_invalidInput(self):
        input_cmd = "SET invalid inv EAXT invalid"
        serialised_input = "*5\r\n$3\r\nSET\r\n$7\r\ninvalid\r\n$3\r\ninv\r\n$4\r\nEAXT\r\n$7\r\ninvalid\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR value is not an integer or out of range\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR value is not an integer or out of range"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

if __name__ == "__main__":
    unittest.main()