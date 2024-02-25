from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
import redis
import json
import uuid

# landing_bp = Blueprint('landing', __name__,)

# @landing_bp.route('/landing')
# def landing_page():
#     return render_template('landing_page.html', user=current_user)


redis_client = redis.Redis(
    host='redis-14820.c322.us-east-1-2.ec2.cloud.redislabs.com', 
    port=14820, 
    db=0,
    password='2Uyb7SiEfayqazk74dJhN39xfrZBPb91',
    decode_responses=True
    )

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    redis_client = current_app.redis_client
    email = None  # Default value

    if request.method == 'POST':
        email = request.form.get('email')
        password_in = request.form.get('password')
        
        user_id = redis_client.get(f'email:{email}')
        if user_id:
            user_data = redis_client.hgetall(f'user:{user_id.decode()}')
            decoded_user_data = {key.decode(): value.decode() for key, value in user_data.items()}
            if user_data:
                stored_password = decoded_user_data.get('password')
                if stored_password is not None:
                    if check_password_hash(stored_password, password_in):
                        user = User(**decoded_user_data)
                        print(current_user.is_authenticated)
                        print(user.get_id())
                        login_user(user, remember=True)  # Log in the user
                        print(current_user.is_authenticated)
                        flash('Logged in successfully!', category='success')
                        return redirect(url_for('landing.landing_page'))
                    else:
                        flash('Incorrect email or password. Please try again.', category='error')
                else:
                    flash('Password not found for this user.', category='error')
            else:
                flash('User data not found.', category='error')
        else:
            flash('Email does not exist.', category='error')

    # Render the login template for GET requests
    return render_template('login.html', user=current_user)
        # Only pass email to the template if the user is logged in
        # email = current_user.email if current_user.is_authenticated else None
        # return render_template("login.html", email=email)

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
        user_location = request.form.get('state')

        # #check password
        upper = False
        lower = False
        num = False
        space = False 
        for i in password1:
            if(i.isupper()): 
                upper = True
            elif(i.islower()):
                lower = True
            elif(i.isdigit()):
                num = True
            elif(i.isspace()):
                space = True
        if redis_client.exists(f'email:{email}'):
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif (len(password1) < 7 or not upper or not lower or not num or space):
            flash('Password invalid', category='error')
        else:
            #user_location = str(location)
            #print(user_location)
            score_list = ""
            score_avg = 0.0
            access_token_generate = str(uuid.uuid1())
            user_id = email
            string_location = str(user_location)
            hashed_password = generate_password_hash(password1)
            redis_client.hmset(f'user:{user_id}', {'email': email, 'password': hashed_password, 'first_name': first_name, 'access_token': access_token_generate, 'scores': score_list, 'score_avg':score_avg, 'location': string_location}) 
            redis_client.set(f'email:{email}', user_id)
            flash('Account created successfully! You can now log in.', category='success')
            newUser = User(email, hashed_password, first_name, access_token_generate, score_list, score_avg, string_location)
            login_user(newUser, remember=True)
            return redirect('/landing')
    
    return render_template("sign_up.html", user=current_user)