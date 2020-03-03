from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models.user import User
from models.images import Image
from flask_login import login_user, logout_user, current_user, login_required
from instagram_web.util.s3_uploader import upload_file_to_s3
# from
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
        got_image = Image.select().where(Image.user_id == current_user.id)
        return render_template('sessions/new.html', currentuser_name=current_user.name, got_image=got_image)
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
    if not query_email and len(new_email) != 0:
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


@sessions_blueprint.route('/upload', methods=['POST'])
@login_required
def profimg_upload():
    file = request.files.get('profile_image')
    if not 'profile_image' in request.files:
        flash('no image has been provided', 'danger')
        return redirect(url_for('sessions.prof_info', id=current_user.id))

    if not upload_file_to_s3(file):
        file.filename = secure_filename(file.filename)
        flash('Oops! Something went wrong while uploading', 'warning')
        return redirect(url_for('sessions.prof_info', id=current_user.id))

    # else:
    #     flash('upload complete')
    #     return redirect(url_for('sessions.prof_info', id=current_user.id))

    else:
        user = User.get_or_none(User.id == current_user.id)
        user.profile_image = file.filename

        user.save()

        flash('successfully added profile image!', 'success')
        return redirect(url_for('sessions.prof_info', id=current_user.id))


@sessions_blueprint.route('/new/upload', methods=['POST'])
@login_required
def usr_img_upload():
    usr_img = request.files.get('user_image')
    if not 'user_image' in request.files:
        flash('no image has been provided', 'danger')
        return redirect(url_for('sessions.new'))

    if not upload_file_to_s3(usr_img):
        file.filename = secure_filename(usr_img.filename)
        flash('Oops! Something went wrong while uploading', 'warning')
        return redirect(url_for('sessions.new'))

    else:
        user = User.get_or_none(User.id == current_user.id)
        caption = request.form.get('img_caption')
        user_img = Image(
            user=user.id, user_img=usr_img.filename, caption=caption)
        user_img.save()
        flash('Image successfully uploaded!', 'success')
        return redirect(url_for('sessions.new'))
