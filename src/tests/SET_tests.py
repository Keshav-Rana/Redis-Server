import unittest
from services.RESPService import RESPService
from services.Redis import Redis
from services.CommandService import CommandService

class SET_tests(unittest.TestCase):
    def setUp(self):
        self.resp_service = RESPService()
        self.redis_db = Redis()

    def test_keyWithDoubleQuotes(self):
        input_cmd = 'SET "test" val'
        serialised_input = "*3\r\n$3\r\nSET\r\n$4\r\ntest\r\n$3\r\nval\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "+OK\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "OK"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_valueWithDoubleQuotes(self):
        input_cmd = 'SET test "val"'
        serialised_input = "*3\r\n$3\r\nSET\r\n$4\r\ntest\r\n$3\r\nval\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "+OK\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()

        response_displayed_to_user = "OK"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_keyWithSingleQuotes(self):
        input_cmd = "SET 'test' val"
        serialised_input = "*3\r\n$3\r\nSET\r\n$4\r\ntest\r\n$3\r\nval\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "+OK\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "OK"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_valueWithSingleQuotes(self):
        input_cmd = "SET test 'val'"
        serialised_input = "*3\r\n$3\r\nSET\r\n$4\r\ntest\r\n$3\r\nval\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "+OK\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "OK"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_noValue(self):
        input_cmd = "SET val"
        serialised_input = "*2\r\n$3\r\nSET\r\n$3\r\nval\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        # check if appropriate error message is returned
        response_from_redis = "-ERR wrong number of arguments for 'set' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR wrong number of arguments for 'set' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_noArguments(self):
        input_cmd = "SET"
        serialised_input = "*1\r\n$3\r\nSET\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        # check if appropriate error message is returned
        response_from_redis = "-ERR wrong number of arguments for 'set' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR wrong number of arguments for 'set' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

if __name__ == "__main__":
    unittest.main()