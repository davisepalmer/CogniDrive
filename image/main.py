import asyncio
import random
from websockets.sync.client import connect

async def handler(websocket):
    print("Starting server")
    while True:
        message = await websocket.recv()
        print("Analyzing " + message)
        #message.split()
        await asyncio.sleep(random.uniform(0.5, 2))
        score = await run(message)
        await websocket.send("j712j:" + score)

async def main():
    with connect("ws://localhost:8081/supersecretimageprocessor") as websocket:
        websocket.send("test1=" + await run())
        while True:
            id = input("Enter job id: ")
            id = id + "=" + await run()
            websocket.send(id)
        await asyncio.Future()

async def run():
    return "57"

if __name__ == "__main__":
    asyncio.run(main())