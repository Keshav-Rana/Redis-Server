import socket
from services.CommandService import CommandService
from services.RESPService import RESPService
from services.Redis import Redis

HOST = "localhost"
PORT = 6379

# create server socket using TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket
server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

try:
    while True:
        # accept connection
        client_socket, client_addr = server_socket.accept()
        print(f"Connection from {client_addr} has been established.")

        # receive data from client
        data = client_socket.recv(1024)

        if not data:
            break

        decoded_data = data.decode('utf-8')
        splitted_data = decoded_data.split('\r\n')

        print(f"Received data from client: {splitted_data}")

        cmdService = CommandService(splitted_data)
        response = cmdService.makeResponse()

        # deserialise response using RESP
        response = RESPService.deserialiser(response)

        # send response to client using client socket
        client_socket.sendall(response.encode('utf-8'))

except KeyboardInterrupt:
    print("Shutting down the server...")

finally:
    server_socket.close()