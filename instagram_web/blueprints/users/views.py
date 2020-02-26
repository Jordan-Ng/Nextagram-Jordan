from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from models.user import User
from werkzeug.security import generate_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new/create', methods=['POST'])
def user_create():
    name_input = request.form.get('user_name')
    email_input = request.form.get('email_address')
    pass_input = request.form.get('password')
    hashed_pw = generate_password_hash(pass_input)
    new_user = User(
        name=name_input, email=email_input, password=pass_input)

    if new_user.save():
        flash('Successfully signed up!', 'success')
        return redirect(url_for('users.new'))
    else:
        for error in new_user.errors:
            flash(error, 'danger')
        return render_template('users/new.html', errors=new_user.errors)


@users_blueprint.route('/login', methods=['GET'])
def login_page():
    return render_template('users/login.html')
    # pass


@users_blueprint.route('/login/verify', methods=['POST'])
def verif_login():
    username_get = User.get_or_none(User.name == request.form.get('user_name'))
    if username_get and username_get.password == request.form.get('password'):
        flash('you are logged in!', 'success')
        session['user'] = username_get.name
        # return f"<h1>{username_get.name}'s page</h1>"
        return redirect(url_for('users.prof_show'))
    else:
        flash("username and/or password is incorrect, please try again", "danger")
        return redirect(url_for('users.login_page'))

# hello
@users_blueprint.route('/profile', methods=["GET"])
def prof_show():
    if "user" in session:
        user = session['user']
        return f'<h1>logged in as {user}<h1>'
    else:
        return redirect(url_for('users.login_page'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
