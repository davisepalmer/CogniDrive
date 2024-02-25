from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
#from .models import Leaderboard, User
import json
import redis

redis_client = redis.Redis(
    host='redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com', 
    port=14820, 
    db=0,
    password='2Uyb7SiEfayqazk74dJhN39xfrZBPb91')

views = Blueprint('views', __name__)

def getLeaderboard():
    # Get the top users from Redis
    userlist = []
    for key in redis_client.scan_iter("user:*"):
        user_data = redis_client.hgetall(key.decode())
        #print(user_data)
        decoded_user_data = {key.decode(): value.decode() for key, value in user_data.items()}
        score = decoded_user_data.get('score_avg')
        userlist.append((float(str(decoded_user_data.get('score_avg'))),decoded_user_data.get('first_name')))
        userlist.sort(key=lambda a: a[0], reverse=True)
    return userlist
def getStaterank():
    elements = {}
    cursor = 0
    while True:
        # Scan the hash to retrieve fields with a certain value
        cursor, data = redis_client.hscan(0, cursor, match=f"*{current_user.location}*")
        # Add matching fields to the dictionary
        for key, val in data.items():
            elements[key.decode()] = val.decode()
        # Break the loop if cursor is 0, indicating end of scan
        if cursor == 0:
            break
    return elements
def getStaterank_size():
    elements = redis_client.lrange('my_list', 0, -1)  # Get all elements from the list
    subset = [element for element in elements if element == current_user.location]
    return len(subset)


@views.route('/leaderboard', methods=['GET', 'POST'])
@login_required
def leaderboard():
    print(current_user.location)
    print("loc", current_user.location)
    return render_template('leaderboard.html', user=current_user, leaderboard=getLeaderboard(), stateboard=getStaterank(), state_rank_size=getStaterank_size())