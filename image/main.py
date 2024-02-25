import random
import time
from websockets.sync.client import connect

#import detect

def handler(websocket):
    print("Starting server")
    while True:
        message = websocket.recv()
        print("Analyzing " + message)
        if message == "test2.jpg":
          analyze('test2.jpg')
          continue
        parse = message.split  ("=")
        score = analyze("./temp/" + parse[0] + ".jpg")
        websocket.send("j712j=" + score)

def main():
    with connect("ws://localhost:8081/supersecretimageprocessor") as websocket:
        websocket.send("test1=" + analyze("test2.jpg"))
        handler(websocket)
        #await asyncio.Future()

def analyze(filename):
    return "asdas"
    #return str(detect.run(source=filename))

if __name__ == "__main__":
    main()