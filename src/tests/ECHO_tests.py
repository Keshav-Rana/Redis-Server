import unittest
from services.RESPService import RESPService
from services.CommandService import CommandService
from services.Redis import Redis

class ECHO_tests(unittest.TestCase):
    def setUp(self):
        self.resp_service = RESPService()
        self.redis_db = Redis()

    def test_messageInDoubleQuotes(self):
        input_cmd = 'ECHO "hello world"'
        serialised_input = "*2\r\n$4\r\nECHO\r\n$11\r\nhello world\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "$11\r\nhello world\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '"hello world"'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_messageInSingleQuotes(self):
        input_cmd = "ECHO 'testing 121'"
        serialised_input = "*2\r\n$4\r\nECHO\r\n$11\r\ntesting 121\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "$11\r\ntesting 121\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '"testing 121"'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_messagewithNoQuotes(self):
        input_cmd = "ECHO testing12345"
        serialised_input = "*2\r\n$4\r\nECHO\r\n$12\r\ntesting12345\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "$12\r\ntesting12345\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '"testing12345"'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_invalidMessage(self):
        input_cmd = "ECHO test '2'"
        serialised_input = "*3\r\n$4\r\nECHO\r\n$4\r\ntest\r\n$1\r\n2\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)
        
        # check if exception was thrown
        response_from_redis = "-ERR wrong number of arguments for 'echo' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR wrong number of arguments for 'echo' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_emptyString(self):
        input_cmd = "ECHO ''"
        input_cmd_two = 'ECHO ""'
        serialised_input = "*2\r\n$4\r\nECHO\r\n$0\r\n\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)
        self.assertEqual(self.resp_service.serialiser(input_cmd_two), serialised_input)

        response_from_redis = "$0\r\n\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '""'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

if __name__ == "__main__":
     unittest.main()