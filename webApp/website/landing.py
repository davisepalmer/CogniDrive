from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user, current_user 

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/landing')
def landing_page():
    print(current_user.is_authenticated)
    return render_template('landing_page.html', user=current_user)