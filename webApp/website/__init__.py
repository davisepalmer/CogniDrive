from flask import Flask, redirect, Blueprint, request, url_for
from os import path
from flask_login import LoginManager, current_user, login_required
import redis
from .landing import landing_bp
redis_client = redis.Redis(
    host='redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com', 
    port=14820, 
    db=0,
    password='2Uyb7SiEfayqazk74dJhN39xfrZBPb91'
    )
#from . import create_app
#redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com:14820

def create_app(redis_client):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SHAQUILLEONEAL'


    from .views import views
    from .auth import auth

    app.redis_client = redis_client
    app.register_blueprint(views)
    app.register_blueprint(auth)

    from .models import User, Leaderboard

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect unauthorized users to the login page
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # Load user from Redis
        user_data = redis_client.hgetall('user:'+id)
        if user_data:
            user_data_str = {key.decode(): value.decode() for key, value in user_data.items()}
            return User(**user_data_str)
        return None

    @app.route('/')
    def landing_redirect():
        if current_user.is_authenticated:
            return redirect(url_for('views.leaderboard'))  # Redirect to the leaderboard page
        else:
            return redirect(url_for('landing.landing_page'))

    return app


def register_blueprints(app):
    app.register_blueprint(landing_bp)  # Register the landing_bp blueprint

# Call the function to create the app and register the blueprints
app = create_app(redis_client)
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)