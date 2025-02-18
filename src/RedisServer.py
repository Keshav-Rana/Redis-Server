import socket

HOST = "localhost"
PORT = 6379

# create server socket using TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket
server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

while True:
    # accept connection
    client_socket, client_addr = server_socket.accept()
    print(f"Connection from {client_addr} has been established.")

    # receive data from client
    data = client_socket.recv(1024)

    if not data:
        break

    print("Received data: {data.decode('utf-8')}")

    # send response to client using client socket
    client_socket.sendall("Hello, client!".encode('utf-8'))

    # close the connection
    client_socket.close()