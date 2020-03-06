import config
from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.donations.view import donations_blueprint
from instagram_web.blueprints.follows.views import follows_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import LoginManager, current_user
from models.images import Image
import os
from instagram_web.util.google_auth import oauth
# from models.user import User

assets = Environment(app)
assets.register(bundles)
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(follows_blueprint, url_prefix="/follows")
oauth.init_app(app)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def forbidden(e):
    return render_template('401.html'), 401


@app.route("/")
def home():
    all_image = Image.select().where(Image.user_id != current_user.id)
    return render_template('home.html', all_image=all_image)


@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.get_or_none(User.id == user_id)
