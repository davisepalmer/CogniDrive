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
          dist = analyze("./temp/" + parse[0] + ".jpg")
          score = safety_score(int(parse[2]),int(parse[1]),float(dist))
          websocket.send(parse[0] + "=" + str(score))

def safety_score(spd, spd_limit, follow_dist):
    score = 100
    if (spd - spd_limit) > 0:
        score -= (spd - spd_limit)**2
    if follow_dist < optimal_follow(spd):
        score -= ((optimal_follow(spd) - follow_dist)/2)**2
    return max(score, 0)

def optimal_follow(spd):
    return spd * 1.5

def main():
    with connect("ws://localhost:80/supersecretimageprocessor") as websocket:
        websocket.send("test1=" + analyze("test2.jpg"))
        handler(websocket)
        #await asyncio.Future()

def analyze(filename):
    return str(detect.run(source=filename))

if __name__ == "__main__":
    main()