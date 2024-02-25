import random
import time
from websockets.sync.client import connect

import detect

def handler(websocket):
    print("Starting server")
    while True:
        message = websocket.recv()
        print("Analyzing " + message)
        #message.split()
        time.sleep(1)
        score = analyze(message)
        websocket.send("j712j=" + score)

def main():
    with connect("ws://localhost:80/supersecretimageprocessor") as websocket:
        websocket.send("test1=" + analyze())
        handler(websocket)
        #await asyncio.Future()

def analyze(filename):
    return str(detect.run(source='test2.jpg'))

if __name__ == "__main__":
    main()