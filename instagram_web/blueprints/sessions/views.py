from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import login_user, logout_user, current_user, login_required

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/', methods=['GET'])
def index():
    return render_template('sessions/login.html')


@sessions_blueprint.route('/verify', methods=['POST'])
def verif_login():
    username_get = User.get_or_none(User.name == request.form.get('user_name'))
    if username_get and check_password_hash(username_get.password, request.form.get('password')):
        login_user(username_get)
        flash('you are logged in!', 'success')
        # session['user'] = username_get.name
        return redirect(url_for('sessions.new'))
    else:
        flash("username and/or password is incorrect, please try again", "danger")
        return redirect(url_for('sessions.index'))


@sessions_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    if current_user:
        return render_template('sessions/new.html', currentuser_name=current_user.name)
    # if "user" in session:
    #     user = session['user']
    # return f'<h1>logged in as {user}<h1>'
    # else:
        # return abort()
        # return render_template('403.html')
        # return redirect(url_for('sessions.index'))


@sessions_blueprint.route('/<id>/info')
@login_required
def prof_info(id):
    if current_user:
        return render_template('sessions/profinfo.html', id=current_user.id)


@sessions_blueprint.route('/<id>/update/', methods=['POST'])
@login_required
def email_update(id):

    id = current_user.id
    # user = User.get_by_id(id)
    new_email = request.form.get('email_address')
    current_user.email = new_email

    query_email = User.get_or_none(User.email == new_email)
    # current_user.email = new_email
    if not query_email:
        current_user.save()
        flash("your email was updated successfully!", 'success')
        return redirect(url_for('sessions.new'))
    else:
        flash(
            'Email entered is associated with another account, please try again', 'danger')
        return redirect(url_for('sessions.prof_info', id=current_user.id))
    # if query_email and current_user.id == query_email.id:
    #     current_user.email = new_email
    #     current_user.save()


'''execute way'''
# mod_email = User(email=new_email).where(User.name == current_user.name)
# mod_email = User.update(email=new_email).where(
#     User.name == current_user.name)

# try:
#     # breakpoint()
#     mod_email.execute()
#     # mod_email.save()
#     flash('email updated successfully', 'success')
#     return redirect(url_for('sessions.new'))
# except:
#     flash('something went wrong, try again', 'danger')
#     return redirect(url_for('sessions.prof_info'))


@sessions_blueprint.route('/end', methods=['GET'])
def logout():
    # session.pop('user', None)
    logout_user()
    flash('successfully logged out', 'success')
    return redirect(url_for('sessions.index'))


@sessions_blueprint.route('/<id>/upload', methods=['POST'])
def profimg_upload():
    pass
