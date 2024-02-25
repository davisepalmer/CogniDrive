import random
import time
import os
from websockets.sync.client import connect

import detect

def handler(websocket):
    print("Starting server")
    while True:
        message = websocket.recv()
        print("Analyzing " + message)
        if message == "test2.jpg":
          analyze('test2.jpg')
          continue
        parse = message.split("=")
        if os.path.exists("./temp/" + parse[0] + ".jpg"):
          score = analyze("./temp/" + parse[0] + ".jpg")
          websocket.send(parse[0] + "=" + score)

def main():
    with connect("ws://localhost:80/supersecretimageprocessor") as websocket:
        websocket.send("test1=" + analyze("test2.jpg"))
        handler(websocket)
        #await asyncio.Future()

def analyze(filename):
    return str(detect.run(source=filename))

if __name__ == "__main__":
    main()