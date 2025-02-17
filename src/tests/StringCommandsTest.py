import unittest
from services.RESPService import RESPService
class Tests(unittest.TestCase):
    def setUp(self):
        self.resp_service = RESPService()

    def SETCommandTest(self):
        responseFromRedis = "+OK\r\n"
        expectedOutput = "OK"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)

    def GETCommandTest(self):
        responseFromRedis = "$5\r\nHello\r\n"
        expectedOutput = "Hello"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)

    def DELCommandTest(self):
        responseFromRedis = ":2\r\n"
        expectedOutput = "(integer) 2"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)

    def EXPIRECommandTest(self):
        responseFromRedis = ":1\r\n"
        expectedOutput = "(integer) 1"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)

    def NULLStringTest(self):
        responseFromRedis = "$-1\r\n"
        expectedOutput = "(nil)"
        self.assertEqual(RESPService.deserialiser(responseFromRedis), expectedOutput)