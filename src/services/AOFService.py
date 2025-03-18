# append only file mechanism for handling Redis restart and crash
import aiofiles
# import asyncio
from services.RESPService import RESPService

class AOFService:
    async def append_to_file(self, message):
        # open the file in append mode asynchronously:
        async with aiofiles.open("backup.txt", "a") as file:
            await file.write(message + "\r\n")

    async def replay_commands(self, writer):
        # open the file in read mode asynchronously
        try:
            async with aiofiles.open("backup.txt", "r") as file:
                async for line in file:
                    # only parse non-blank lines
                    line = line.strip()
                    if line:
                        # serialise the line
                        line = RESPService.serialiser(line)
                        writer.write(line.encode('utf-8'))
                        await writer.drain() # ensure data is sent to server
        except FileNotFoundError:
            print("No backup file found. Skipping Replay.")