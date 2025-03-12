import unittest
from services.RESPService import RESPService
from services.Redis import Redis
from services.CommandService import CommandService

class DECR_tests(unittest.TestCase):
    def setUp(self):
        self.resp_service = RESPService()
        self.redis_db = Redis()
        # add mock data in db
        self.redis_db.set("test", "1")
        self.redis_db.set("inv", "invalid")

    def test_normalCase(self):
        # increment a value of a key
        input_cmd = "DECR test"
        serialised_input = "*2\r\n$4\r\nDECR\r\n$4\r\ntest\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        # value of the key after increment
        response_from_redis = ":0\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '(integer) 0'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_edgeCase(self):
        # increment a value where the key does not exist, first set it to 0 then decrement
        input_cmd = "DECR test2"
        serialised_input = "*2\r\n$4\r\nDECR\r\n$5\r\ntest2\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        # value of the key after increment
        response_from_redis = ":-1\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '(integer) -1'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_invalidCase(self):
        # try to increment a value which is not convertable to integer
        input_cmd = "DECR inv"
        serialised_input = "*2\r\n$4\r\nDECR\r\n$3\r\ninv\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        # value of the key after increment
        response_from_redis = "-ERR value is not an integer or out of range\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = '(error) ERR value is not an integer or out of range'
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_invalidCase2(self):
        # try to increment values of two keys in single command
        input_cmd = "DECR test2 test3"
        serialised_input = "*3\r\n$4\r\nDECR\r\n$5\r\ntest2\r\n$5\r\ntest3\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        # try to run DECR command without any arguments
        input_cmd_two = "DECR"
        serialised_input_two = "*1\r\n$4\r\nDECR\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd_two), serialised_input_two)

        # value of the key after increment - first case
        response_from_redis = "-ERR wrong number of arguments for 'decr' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        # error - second case
        response_from_redis_two = "-ERR wrong number of arguments for 'decr' command\r\n"
        # split serialised data
        splitted_data_two = self.resp_service.serialiser(input_cmd_two).split('\r\n')
        cmd_service_two = CommandService(splitted_data_two, self.redis_db)
        response_two = cmd_service_two.makeResponse()
        self.assertEqual(response_two, response_from_redis_two)

        response_displayed_to_user = "(error) ERR wrong number of arguments for 'decr' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

        response_displayed_to_user_two = "(error) ERR wrong number of arguments for 'decr' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data_two[2], response_two), response_displayed_to_user_two)

if __name__ == "__main__":
    unittest.main()