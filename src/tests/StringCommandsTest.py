import unittest
from services.RESPService import RESPService
class Tests(unittest.TestCase):
    def setUp(self):
        self.resp_service = RESPService()

    # set key value in redis
    def SETCommandTest(self):
        responseFromRedis = "+OK\r\n"
        expectedOutput = "OK"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)

    # retrieve key value
    def GETCommandTest(self):
        responseFromRedis = "$5\r\nHello\r\n"
        expectedOutput = "Hello"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)

    # delete key value
    def DELCommandTest(self):
        responseFromRedis = ":2\r\n"
        expectedOutput = "(integer) 2"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)

    # set an expiry for key value
    def EXPIRECommandTest(self):
        responseFromRedis = ":1\r\n"
        expectedOutput = "(integer) 1"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)

    # handle case when we try to access non existent key
    def NULLStringTest(self):
        responseFromRedis = "$-1\r\n"
        expectedOutput = "(nil)"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)