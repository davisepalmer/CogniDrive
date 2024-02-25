from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Leaderboard, User
import json
import redis

redis_client = redis.Redis(
    host='redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com', 
    port=14820, 
    db=0,
    password='2Uyb7SiEfayqazk74dJhN39xfrZBPb91')

views = Blueprint('views', __name__)

@views.route('/landing')
def landing_page():
    return render_template('landing_page.html', user=current_user)
