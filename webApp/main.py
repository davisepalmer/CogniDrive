
from website import create_app, register_blueprints
import redis

# Create a Redis client
#redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com:14820
redis_client = redis.Redis(
    host='redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com', 
    port=14820, 
    db=0,
    password='2Uyb7SiEfayqazk74dJhN39xfrZBPb91')

# Create the Flask app
app = create_app(redis_client)

# Register blueprints
register_blueprints(app)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)