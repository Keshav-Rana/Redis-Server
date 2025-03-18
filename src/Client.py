# asynchronous version
import asyncio
from services.RESPService import RESPService

async def send_message():
    HOST = "localhost"
    PORT = 6379

    # Open connection asynchronously and assign StreamReader and StreamWriter objs
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print("Connected to Redis Server")

    try:
        while True:
            # Get input from user
            message = input()
            # Send message to the server
            message = RESPService.serialiser(message)
            # sends the message but does not wait for tranmission to complete
            writer.write(message.encode())
            await writer.drain()  # Ensure the data is sent i.e. the write buffer is completely flushed

            # Receive a response from the server
            response = await reader.read(1024)
            print(f"{response.decode()}")

    except KeyboardInterrupt:
        print("Shutting down the client...")

    except ConnectionError as e:
        print(f"Connection Error: {e}")

    finally:
        writer.close() # initiates the closing process
        await writer.wait_closed() # waits for connection to be completely closed, preventing unexpected behavior

# Run the async function
asyncio.run(send_message()) # sets up event loop, runs the specified coroutine and then cleans up loop

