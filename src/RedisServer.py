# asynchronous version
import asyncio
from services.CommandService import CommandService
from services.RESPService import RESPService
from services.Redis import Redis
from services.AOFService import AOFService

HOST = "localhost"
PORT = 6379

# Create redis database
db = Redis()
# create AOF service instance
aof_service = AOFService()

async def handle_client(reader, writer):
    client_addr = writer.get_extra_info('peername')

    try:
        while True:
            # Read data from the client
            data = await reader.read(1024)
            if not data:
                break

            decoded_data = data.decode('utf-8')
            splitted_data = decoded_data.split('\r\n')

            cmdService = CommandService(splitted_data, db)
            response = cmdService.makeResponse()

            if response is not None and response != "":
                # Deserialize response using RESP and send back to the client
                response = RESPService.deserialiser(splitted_data[2], response)
                writer.write(response.encode('utf-8'))
                await writer.drain()  # Ensure data is sent

    except ConnectionError:
        print(f"Connection with {client_addr} closed due to connection error.")

    except Exception as e:
        print(f"Error handling request from {client_addr}: {e}")

    finally:
        # print(f"Closing connection with {client_addr}")
        writer.close()
        await writer.wait_closed()


async def main():
    # create an asynchronous factory TCP server and pass in our callback function - handle_client
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"Server is listening on {HOST}:{PORT}")

    # replay commands from the backup file
    print("Replaying commands from backup...")
    reader, writer = await asyncio.open_connection(HOST, PORT)
    await aof_service.replay_commands(writer)
    writer.close()
    await writer.wait_closed()
    
    # use the server as asynchronous context manager which prepares the server for operation and ensuring graceful exit
    async with server:
        # serve_forever is async coroutine that tells server to keep running indefinitely until it is externally canceled or shut down
        await server.serve_forever()


# Run the asyncio server
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nShutting down the server...")
