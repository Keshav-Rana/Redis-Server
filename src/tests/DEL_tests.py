import unittest
from services.Redis import Redis
from services.CommandService import CommandService
from services.RESPService import RESPService

class EXISTS_tests(unittest.TestCase):
    def setUp(self):
        self.resp_service = RESPService()
        self.redis_db = Redis()
        # add mock data in redis db
        self.redis_db.set("test", "val")
        self.redis_db.set("test2", "val2")
        self.redis_db.set("test3", "val3")
        self.redis_db.set("test4", "val4")
        self.redis_db.set("test5", "val5")

    def test_oneKey(self):
        input_cmd = "DEL test"
        serialised_input = "*2\r\n$3\r\nDEL\r\n$4\r\ntest\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = ":1\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(integer) 1"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

        # check that the deleted key does not exist in the db
        self.assertEqual(None, self.redis_db.get("test"))

    def test_oneKeyButDoesNotExist(self):
        input_cmd = "DEL invalid"
        serialised_input = "*2\r\n$3\r\nDEL\r\n$7\r\ninvalid\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = ":0\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(integer) 0"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

    def test_multipleKeys(self):
        input_cmd = "DEL test2 test3 test4"
        serialised_input = "*4\r\n$3\r\nDEL\r\n$5\r\ntest2\r\n$5\r\ntest3\r\n$5\r\ntest4\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = ":3\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(integer) 3"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

        # check if the inserted key exists in db
        self.assertEqual(None, self.redis_db.get("test2"))
        self.assertEqual(None, self.redis_db.get("test3"))
        self.assertEqual(None, self.redis_db.get("test4"))

    def test_multipleKeysbutSomeExists(self):
        input_cmd = "DEL test5 inv2 inv3"
        serialised_input = "*4\r\n$3\r\nDEL\r\n$5\r\ntest5\r\n$4\r\ninv2\r\n$4\r\ninv3\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = ":1\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(integer) 1"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

        # check if key - test5 was deleted
        self.assertEqual(None, self.redis_db.get("test5"))

    # sad path
    def test_noKeys(self):
        input_cmd = "DEL"
        serialised_input = "*1\r\n$3\r\nDEL\r\n"
        self.assertEqual(self.resp_service.serialiser(input_cmd), serialised_input)

        response_from_redis = "-ERR wrong number of arguments for 'exists' command\r\n"
        # split serialised data
        splitted_data = self.resp_service.serialiser(input_cmd).split('\r\n')
        cmd_service = CommandService(splitted_data, self.redis_db)
        response = cmd_service.makeResponse()
        self.assertEqual(response, response_from_redis)

        response_displayed_to_user = "(error) ERR wrong number of arguments for 'exists' command"
        self.assertEqual(self.resp_service.deserialiser(splitted_data[2], response), response_displayed_to_user)

if __name__ == "__main__":
    unittest.main()