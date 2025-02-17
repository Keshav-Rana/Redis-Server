from services.RESPService import RESPService
from src.services.redisServer import redisServer

def main():
    input_val = input()
    input_val = RESPService.serialiser(input_val)
    response = redisServer.processInput(input_val)
    response = RESPService.deserialiser(response)
    print(response)