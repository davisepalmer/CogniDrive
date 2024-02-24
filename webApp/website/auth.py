from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import redis

redis_client = redis.Redis(
    host='redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com', 
    port=14820, 
    db=0,
    password='2Uyb7SiEfayqazk74dJhN39xfrZBPb91')

auth = Blueprint('auth', __name__)
# def init_auth(redis_client):
@auth.route('/login', methods=['GET', 'POST'])
def login():
    redis_client = current_app.redis_client
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_id = redis_client.get(f'email:{email}')
        if user_id:
            user_data = redis_client.hgetall(f'user:{user_id.decode()}')
            if user_data and check_password_hash(user_data.get('password'), password):
                user = User(**user_data)
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect('/landing')
            else:
                flash('Incorrect email or password. Please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", email=current_user.email)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect('/login')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if redis_client.exists(f'email:{email}'):
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user_id = redis_client.incr('user_id_counter')
            hashed_password = generate_password_hash(password1)
            redis_client.hmset(f'user:{user_id}', {'id': user_id, 'email': email, 'password': hashed_password, 'first_name': first_name})
            redis_client.set(f'email:{email}', user_id)
            flash('Account created successfully! You can now log in.', category='success')
            return redirect('/login')

    return render_template("sign_up.html", user=current_user)
