import asyncio
from websockets.sync.client import connect

async def handler(websocket):
    while True:
        message = await websocket.recv()
        print("Analyzing " + message)
        run(message)

async def main():
    await asyncio.Future()

def run():
    return

if __name__ == "__main__":
    asyncio.run(main())