from flask import Blueprint, render_template, url_for, request, flash, redirect
# from models.user import User
# from models.images import Image
# from flask_login import login_user

donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


@donations_blueprint.route('/', methods=['GET'])
def index():
    return render_template('donations/donate.html')
