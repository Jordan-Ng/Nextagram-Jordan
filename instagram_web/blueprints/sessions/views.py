from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from models.user import User

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/', methods=['GET'])
def index():
    return render_template('sessions/login.html')


@sessions_blueprint.route('/verify', methods=['POST'])
def verif_login():
    username_get = User.get_or_none(User.name == request.form.get('user_name'))
    if username_get and username_get.password == request.form.get('password'):
        flash('you are logged in!', 'success')
        session['user'] = username_get.name
        return redirect(url_for('sessions.new'))
    else:
        flash("username and/or password is incorrect, please try again", "danger")
        return redirect(url_for('sessions.index'))


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    if "user" in session:
        user = session['user']
        return render_template('sessions/new.html', user=user)
        # return f'<h1>logged in as {user}<h1>'
    else:
        return redirect(url_for('sessions.index'))


@sessions_blueprint.route('/end', methods=['GET'])
def logout():
    session.pop('user', None)
    flash('successfully logged out', 'success')
    return redirect(url_for('sessions.index'))
