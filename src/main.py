from src.services.resp import resp
from src.services.redisServer import redisServer

def main():
    # take user input
    input_val = input()
    # serialise it using our RESP protocol
    input_val = resp.serialiser(input_val)
    # send it to the server
    # receive a response
    response = redisServer.processInput(input_val)
    # deserialise the response
    response = resp.deserialiser(response)
    # print the response
    print(response)