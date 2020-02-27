from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from models.user import User


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
    new_user = User(
        name=name_input, email=email_input, password=pass_input)

    if new_user.save():
        flash('Successfully signed up!', 'success')
        return redirect(url_for('users.new'))
    else:
        for error in new_user.errors:
            flash(error, 'danger')
        return render_template('users/new.html', errors=new_user.errors)


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
