from flask import Blueprint, render_template
from flask_login import current_user

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/landing')
def landing_page():
    return render_template('landing_page.html', user=current_user)