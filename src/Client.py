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

try:
    while True:
        # get input from user
        message = input()

        # send message to server
        message = RESPService.serialiser(message)
        # print(message)

        client_socket.sendall(message.encode())

        # receive a response from the server
        response = client_socket.recv(1024)
        print(f"{response.decode()}")

except KeyboardInterrupt:
    print("Shutting down the server...")

except ConnectionError as e:
    print(f"Connection Error: {e}")

finally:
    client_socket.close()