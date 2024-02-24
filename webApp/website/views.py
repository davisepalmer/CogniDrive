from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Leaderboard, User
import json

views = Blueprint('views', __name__)

# @views.route('/landing')
# def landing_page():
#     return render_template('landing_page.html', user=current_user)

@views.route('/leaderboard', methods=['GET', 'POST'])
@login_required
def leaderboard():
    if request.method == 'POST': 
        # Handle form submission if needed
        pass
    leaderboard_data = Leaderboard.get_leaderboard(limir=10)

    return render_template('leaderboard.html', user=current_user, leaderboard=leaderboard)
