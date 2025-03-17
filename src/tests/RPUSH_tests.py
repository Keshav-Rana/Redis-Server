import unittest
from services.RESPService import RESPService
from services.CommandService import CommandService
from services.Redis import Redis

class RPUSH_tests(unittest.TestCase):
    def setUp(self):
        self.resp_service = RESPService()
        self.redis_db = Redis()
        self.redis_db.set("mockKey", "4")

    # adding three values to list
    def test_normalCase(self):
        input_cmd = 'RPUSH test one two three'
        serialised_input = "*5\r\n$5\r\nRPUSH\r\n$4\r\ntest\r\n$3\r\none\r\n$3\r\ntwo\r\n$5\r\nthree\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = ":3\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '(integer) 3'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

        # assert list size and elements
        self.assertEqual(len(self.redis_db.get("test")), 3)
        self.assertEqual(self.redis_db.get("test")[2], "three")
        self.assertEqual(self.redis_db.get("test")[1], "two")
        self.assertEqual(self.redis_db.get("test")[0], "one")

    # no arguments with command
    def test_noArguments(self):
        input_cmd = 'RPUSH test'
        serialised_input = "*2\r\n$5\r\nRPUSH\r\n$4\r\ntest\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR wrong number of arguments for 'rpush' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR wrong number of arguments for 'rpush' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    # adding values to wrong key
    def test_wrongKey(self):
        input_cmd = 'RPUSH mockKey one'
        serialised_input = "*3\r\n$5\r\nRPUSH\r\n$7\r\nmockKey\r\n$3\r\none\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR WRONGTYPE Operation against a key holding the wrong kind of value\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR WRONGTYPE Operation against a key holding the wrong kind of value"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

if __name__ == "__main__":
    unittest.main()