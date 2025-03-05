from services.RESPService import RESPService
# from RedisServer import RedisServer
import socket

HOST = "localhost"
PORT = 6380

# create client socket for sending data
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
client_socket.connect((HOST, PORT))
print("Connected to Redis Server")

# send message to server
message = RESPService.serialiser('SET testKey val EX ab')
print(message)
# test_message = "Hello ji"
client_socket.sendall(message.encode())

# receive a response from the server
response = client_socket.recv(1024)
print(f"{response.decode()}")

client_socket.close()

# def main():
#     # establish connection

#     # all the processing
#     input_val = input()
#     input_val = RESPService.inputSerialiser(input_val)
#     response = RedisServer.processInput(input_val)
#     response = RESPService.outputDeserialiser(response)
#     print(response)
# 