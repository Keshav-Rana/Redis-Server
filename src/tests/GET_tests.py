import unittest
from services.RESPService import RESPService
from services.Redis import Redis
from services.CommandService import CommandService

class GET_tests(unittest.TestCase):
    def setUp(self):
        self.resp_service = RESPService()
        self.redis_db = Redis()
        # create mock data in redis
        self.redis_db.set("test", "val")

    def test_keyInSingleQuotes(self):
        input_cmd = "GET 'test'"
        serialised_input = "*2\r\n$3\r\nGET\r\n$4\r\ntest\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "$3\r\nval\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '"val"'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_keyInDoubleQuotes(self):
        input_cmd = 'GET "test"'
        serialised_input = "*2\r\n$3\r\nGET\r\n$4\r\ntest\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "$3\r\nval\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '"val"'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_normalKey(self):
        input_cmd = "GET test"
        serialised_input = "*2\r\n$3\r\nGET\r\n$4\r\ntest\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "$3\r\nval\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '"val"'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_extraArguments(self):
        input_cmd = "GET test extra"
        serialised_input = "*3\r\n$3\r\nGET\r\n$4\r\ntest\r\n$5\r\nextra\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR wrong number of arguments for 'get' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR wrong number of arguments for 'get' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_noArguments(self):
        input_cmd = "GET"
        serialised_input = "*1\r\n$3\r\nGET\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR wrong number of arguments for 'get' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR wrong number of arguments for 'get' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_nonExistingKey(self):
        input_cmd = "GET nonExistingKey"
        serialised_input = "*2\r\n$3\r\nGET\r\n$14\r\nnonExistingKey\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "$-1\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        print(splitted_data)
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '(nil)\r\n'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

if __name__ == '__main__':
    unittest.main()