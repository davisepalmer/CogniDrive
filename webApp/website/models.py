
import redis

# Connect to Redis
#redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com:14820
redis_client = redis.Redis(
    host='redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com',
    port=14820, 
    db=0,
    password='2Uyb7SiEfayqazk74dJhN39xfrZBPb91')

class User:
    def __init__(self, email, password, first_name):
        self.id = None  # We'll assign the ID later
        self.email = email
        self.password = password
        self.first_name = first_name
        self.access_token = None

    def save(self):
        # Generate a unique ID for the user
        self.id = redis_client.incr('user_id_counter') #increments so new id every time

        # Check if email is unique
        if redis_client.sismember('emails', self.email):
            raise ValueError('Email already exists')
        
        # Save the user data to Redis
        user_data = {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'access_token': self.access_token
        }
        redis_client.hmset(f'user:{self.id}', user_data)
        
        # Add email to set to enforce uniqueness
        redis_client.sadd('emails', self.email)

    @classmethod
    def load(cls, user_id):
        # Load user data from Redis
        user_data = redis_client.hgetall(f'user:{user_id}')
        if user_data:
            return cls(**user_data)
        return None

class Leaderboard:
    @staticmethod
    def add_score(user_id, score):
        redis_client.zadd('leaderboard', {user_id: score})

    @staticmethod
    def get_leaderboard(limit=10):
        # Retrieve the leaderboard from Redis
        leaderboard = redis_client.zrevrange('leaderboard', 0, limit - 1, withscores=True)
        return leaderboard

    @staticmethod
    def get_user_score(user_id):
        # Get the score of a specific user from the leaderboard
        score = redis_client.zscore('leaderboard', user_id)
        return score

    @staticmethod
    def get_user_rank(user_id):
        # Get the rank of a specific user in the leaderboard
        rank = redis_client.zrevrank('leaderboard', user_id)
        return rank + 1 if rank is not None else None