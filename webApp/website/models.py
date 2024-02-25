
import redis
from flask_login import UserMixin
import uuid
import json


# Connect to Redis
#redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com:14820
redis_client = redis.Redis(
    host='redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com',
    port=14820, 
    db=0,
    password='2Uyb7SiEfayqazk74dJhN39xfrZBPb91')

class User(UserMixin):
    def __init__(self, email, password, first_name, access_token, scores, score_avg):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.access_token = access_token
        self.scores = scores
        self.score_avg = score_avg
        #pass IOHB89n

    @staticmethod
    def load_user(user_id):
        # Load user data from Redis
        user_data = redis_client.hgetall('user:'+id)
        if user_data:
            # You should only return the User object if it exists and is active
            # In Flask-Login, an active user is represented by having is_active property as True
            user = User(**user_data)
            user.is_active = True  # Assuming your User class has an is_active attribute
            return user
        return None

    @property
    def is_authenticated(self):
        # Assuming all users are authenticated
        return True

    @property
    def is_active(self):
        # Assuming all users are active
        return True

    @property
    def is_anonymous(self):
        # Assuming no users are anonymous
        return False

    def get_id(self):
        return self.email


    def save(self):
        # Check if email is unique
        if redis_client.sismember('emails', self.email):
            raise ValueError('Email already exists')

        # Hash the password
        hashed_password = generate_password_hash(self.password)

        # Save the user data to Redis with the hashed password
        user_data = {
            'email': self.email,
            'password': hashed_password,
            'first_name': self.first_name,
            'access_token': self.access_token,
            'scores': self.scores,
            'score_avg': self.score_avg,
        }
        redis_client.hmset(f'user:{self.email}', user_data)
        
        # Add email to set to enforce uniqueness
        redis_client.sadd('emails', self.email)
